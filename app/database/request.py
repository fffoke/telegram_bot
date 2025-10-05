from app.database.models import async_session, User, Task
from sqlalchemy import select, delete


                        #  Работа с User
# Сохроняем нового User
async def save_user(tg_id):
    async with async_session() as s:
        user = await s.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            s.add(User(tg_id = tg_id))
            await s.commit()

# Получаем всех User
async def all_user():
    async with async_session() as s:    
        return await s.scalars(select(User))
    
# Получаем current_user
async def get_user(tg_id):
    async with async_session() as s:
        user = await s.scalar(select(User).where(User.tg_id == tg_id))
        return user


                        #  Работа с Task
# Вытаскиваем все загаловки Task что бы создать Inline кнопки под текстом 
async def get_tasks_kb(tg_id):
    async with async_session() as s:
        msg = []
        user = await get_user(tg_id)
        tasks = await s.scalars(select(Task).where(Task.user_id == user.id))
        for task in tasks:
            msg.append(task.title)

        last_msg = ''.join(msg)
        return  last_msg

# Делаем запрос в БД и добовляем задачу привязывая её к юзеру
async def add_task(title, des, user):
    async with async_session() as s:
        s.add(Task(title=title, des=des, user=user))
        await s.commit()

# Получаем как обьект все задачи юзера делая запрос в БД
async def get_users_task(user_id):
    async with async_session() as s:
        return await s.scalars(select(Task).where(Task.user_id == user_id))

# Обраотка callback делая запрос в базу получаем des нужного Task 
async def get_task_des(task_id):
    async with async_session() as s:
        task_des = await s.scalar(select(Task).where(Task.id == task_id))
        return task_des
    
# Удаления Task
async def delet_task_by_title(task_id):
    async with async_session() as s:
        await s.execute(delete(Task).where(Task.id == task_id))
        await s.commit()


                    # Работа с планировщиком               
# добовляем время планировщка 
async def set_time(tg_id, hour, min):
    async with async_session() as s:
        user = await s.scalar(select(User).where(User.tg_id == tg_id))
        user.hour = hour
        user.min = min
        await s.commit()


