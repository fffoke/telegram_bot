from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardButton, InlineKeyboardMarkup)
from app.database.request import get_tasks_kb, get_users_task
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Inline кнопки для выбора дня недели 
chose_day = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ПН', callback_data='day_0'), InlineKeyboardButton(text='ВТ', callback_data='day_1')],
    [InlineKeyboardButton(text='СР', callback_data='day_2'), InlineKeyboardButton(text='ЧТ', callback_data='day_3')],
    [InlineKeyboardButton(text='ПТ', callback_data='day_4'), InlineKeyboardButton(text='СБ', callback_data='day_5')]], 
    resize_keyboard=True , input_field_placeholder='Выберете что-то из меню')


# функция для динамического выбора задания из спасика заданий пользователя
async def all_taskss(user_id, callback_data_start):
    keybord = InlineKeyboardBuilder()
    tasks = await get_users_task(user_id=user_id)
    for task in tasks:
        keybord.add(InlineKeyboardButton(text=task.title, callback_data=f'{callback_data_start}_{task.id}'),)
    return keybord.adjust(2).as_markup()


chose_bell = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Деф', callback_data='bell_1')],
    [InlineKeyboardButton(text='ВТ', callback_data='bell_2'), InlineKeyboardButton(text='CБ', callback_data='bell_3')]
], resize_keyboard=True , input_field_placeholder='Выберете что-то из меню')