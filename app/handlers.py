from aiogram import   F, Router
from aiogram.filters import CommandStart , Command
from aiogram.types import Message, CallbackQuery
import config as c
import app.keyboards as kb
from aiogram.types import FSInputFile
import app.fuctions as f
from random import randint
from app.database.request import save_user,add_task, get_user, get_task_des, set_time, delet_task_by_title
from app.midelware import AddTask, AddTime
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()



# Команда /start и добовляем юзера в бд
@router.message(CommandStart())
async def start(message: Message):
    await save_user(message.from_user.id)
    await message.answer(f'''
📚Даник приветствует !  
Этот бот напомнит тебе о парах, расписании и поможет быть в курсе.  
Команда /help расскажет больше. 
''')

# Команда выводи расписания на сегодня
@router.message(Command('today'))
async def today(message: Message):
    lastmg = f.getToday(c.weekday_index)
    ran = randint(1, 36)
    photo = FSInputFile(f'media/images/{ran}.jpg')
    await message.answer_photo(
        photo=photo,
        caption=lastmg,
    )

# Команда выводи расписания на завтра
@router.message(Command('tommorow'))
async def today(message: Message):
    lastmg = f.getToday(0 if c.weekday_index + 1 > 6 else c.weekday_index+1)
    ran = randint(1, 36)
    photo = FSInputFile(f'media/images/{ran}.jpg')
    await message.answer_photo(
        photo=photo,
        caption=lastmg,
    )


# Команда вывода расписания звонков
@router.message(Command('bells'))
async def bells(message: Message):
    await message.answer(f'<b>Выберите день недели</b>',  parse_mode="HTML", reply_markup=kb.chose_bell)

# Команда для вывода расписания на всю неделю
@router.message(Command('all'))
async def start(message: Message):
    msg = []
    for i in range(6):
        msg.append(f'\n{f.text(c.days[i])}\n {f.getToday(i)}')
    lastmsg = ''.join(msg)
    await message.answer(f'{lastmsg}')

# Выбор кастомного дня через Inline кнопки
@router.message(Command('chose_day'))
async def chose_def(message: Message):
    await message.answer('Выберете спецальный день', reply_markup=kb.chose_day)



# Команда help
@router.message(Command('help'))
async def hepl(message: Message):
    await message.answer('''
            📖 Команды бота
🔹 /start — запуск бота, добавление тебя в список пользователей.
🔹 /today — показывает расписание на сегодняшний день.
🔹 /all — выводит расписание на всю неделю.
🔹 /bells — время звонков (расписание звонков).
🔹 /chose_day — для ожного из дней недели
🔹 /set_time — настройка времени для утреней рассылки
🔹 /add_task — добавить задачу
🔹 /get_tasks — просмотр всех задач
🔹 /tomorrow — расписание на завтра.
🔹 /delete_task — удаление задачи.
🔹 /help — список всех доступных команд и их описание.

✨ Дополнительно:

Каждый день утром бот присылает расписание и прогноз погоды.

Перед началом пары приходит напоминание с предметом, временем и кабинетом.

Иногда сообщения сопровождаются гифкой для настроения 🙂''')


# Добавить Задачу
@router.message(Command('add_task'))
async def add_task_tg(message: Message,state: FSMContext):
    await state.set_state(AddTask.title)
    await message.answer('Введите загаловок задания:')

# Роут для получения title для Task
@router.message(AddTask.title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(AddTask.des)
    await message.answer('Введите описания задания:')

# Роут для получения des для Task и его сохронения 
@router.message(AddTask.des)
async def add_des(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    await state.update_data(des=message.text)
    data = await state.get_data()
    task = await add_task(title=data['title'], des=data['des'], user = user)
    await message.answer('Успешно добавили задачу!')
    await state.clear()

# Выбор задачи для её удаления ( удаления на 154... )
@router.message(Command('delete_task'))
async def delete_task(message: Message):
    user = await get_user(message.from_user.id)
    await message.answer(text='Выберет задачу для удаления', reply_markup=await kb.all_taskss(user_id=user.id, callback_data_start='delet_task') )

# Получения всех Заданий 
@router.message(Command('get_tasks'))
async def get_tasks1(message: Message):
    user = await get_user(message.from_user.id)
    await message.answer(text='Все ваши задачи:', reply_markup=await kb.all_taskss(user.id , callback_data_start='add_task'))
# Создаем состояния AddTime и спрашиваем у юзера время
@router.message(Command('set_time'))
async def start_set_time(message: Message, state: FSMContext):
    await state.set_state(AddTime.time)
    await message.answer(text='Отправьте время в котором вам будет проходить утреняя рассылка в формате 00:00')

# Крч как спросили время пытаемся создать задачу если не получается отдаём ошибку 
@router.message(AddTime.time)
async def set_time_hn(message: Message, state: FSMContext):
    try:
        hour = int(message.text.split(':')[0].strip()) 
        min = int(message.text.split(':')[1].strip())
        time = await set_time(tg_id=message.from_user.id, hour=hour, min=min)
    except (ValueError, IndexError):
        await message.answer('Пожайлусто введите время в формате: "00:00" ')
    job_creat = await f.set_job(tg_id=message.from_user.id)
    await message.answer(f'Ваша утряняя расслыка будет приходить в - {hour}:{min}')
    await state.clear()

# callback

@router.callback_query(F.data.startswith('bell_'))
async def get_bell(callback: CallbackQuery):
    index = int(callback.data.split('_')[1])
    msg = c.bell.get(index)
    await callback.message.edit_text(text=msg, parse_mode="HTML")
# Для вывода расписания определенного дня
@router.callback_query(F.data.startswith('day_'))
async def get_day(callback: CallbackQuery):
    index = int(callback.data.split('_')[1])
    msg = f.getToday(index)  # Полчумаеться мы вытаскиваем индекс
    await callback.answer(f'Вы выбрали {c.days[index]}')
    await callback.message.answer(text=msg, show_alert=True)

# Для вывода описания задачи
@router.callback_query(F.data.startswith('add_task'))
async def get_des(callback: CallbackQuery):
    task_id = int(callback.data.split('_')[-1])
    msg = await get_task_des(task_id=task_id)
    await callback.answer(f'Задача {msg.title}')
    await callback.message.answer(f'<b>Описания вашей задачи</b>: {msg.des}', parse_mode='HTML')

# Для удаления Task 
@router.callback_query(F.data.startswith('delet_task_'))
async def  del_task(callback: CallbackQuery):
    task_id = int(callback.data.split('_')[-1])
    try:
        await delet_task_by_title(task_id = task_id)
        await callback.answer(f'Задача удалена')
        await callback.message.answer(f'Задача успешно удалена')
    except IndexError:
        callback.message.answer(';')