import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON_WORKSPACE, LEXICON_RU


# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(
        *args: str,
        width: int = 2,
        **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Создаем объект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text=LEXICON_WORKSPACE['show_tasks_today'],
            callback_data='show_tasks_today_pressed')],
        [InlineKeyboardButton(
            text=LEXICON_WORKSPACE['show_tasks_for_week'],
            callback_data='show_tasks_for_week_pressed')],
        [InlineKeyboardButton(
            text=LEXICON_WORKSPACE['show_all_tasks'],
            callback_data='show_all_tasks_pressed')],
        [InlineKeyboardButton(
            text=LEXICON_WORKSPACE['add_task'],
            callback_data='add_task_pressed')]
    ])


def day_kb() -> InlineKeyboardMarkup:
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
