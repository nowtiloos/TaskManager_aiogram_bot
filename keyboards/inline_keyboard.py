from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_WORKSPACE



# Создаем объекты инлайн-кнопок
show_tasks_today = InlineKeyboardButton(
    text=LEXICON_WORKSPACE['show_tasks_today'],
    callback_data='show_tasks_today_pressed')

show_tasks_for_week = InlineKeyboardButton(
    text=LEXICON_WORKSPACE['show_tasks_for_week'],
    callback_data='show_tasks_for_week_pressed')

show_all_tasks = InlineKeyboardButton(
    text=LEXICON_WORKSPACE['show_all_tasks'],
    callback_data='show_all_tasks_pressed')

add_task = InlineKeyboardButton(
    text=LEXICON_WORKSPACE['add_task'],
    callback_data='add_task_pressed')

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [add_task],
        [show_tasks_today],
        [show_tasks_for_week],
        [show_all_tasks]
    ])
