import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

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


def day_markup():
    markup = InlineKeyboardBuilder()

    # Получаем текущую дату
    today = datetime.now()
    current_day = today.day
    current_month = today.month
    current_year = today.year

    # Получаем количество дней в текущем месяце
    _, num_days = calendar.monthrange(current_year, current_month)

    # Создаем клавиатуру с днями месяца, начиная с текущей даты
    for day in range(current_day, num_days + 1):
        button_text = str(day)
        callback_data = str(datetime(current_year, current_month, day))
        markup.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    return markup.as_markup()
