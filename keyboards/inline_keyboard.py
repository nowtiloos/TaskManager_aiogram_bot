import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import lexicon


# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(*args: str, width: int = 2, **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=lexicon[button] if button in lexicon else button,
                    callback_data=button,
                )
            )
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Создаем объект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=lexicon["add_task"], callback_data="add_task_pressed"
            )
        ],
        [
            InlineKeyboardButton(
                text=lexicon["show_tasks_today"],
                callback_data="show_tasks_today_pressed",
            )
        ],
        [
            InlineKeyboardButton(
                text=lexicon["show_tasks_for_week"],
                callback_data="show_tasks_for_week_pressed",
            )
        ],
        [
            InlineKeyboardButton(
                text=lexicon["show_all_tasks"], callback_data="show_all_tasks_pressed"
            )
        ],
    ]
)


def days_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    # Получаем текущую дату
    today = datetime.now()
    current_day = today.day
    current_month = today.month
    current_year = today.year

    # Создаем клавиатуру с 21 днём, начиная с текущей даты
    for _ in range(21):
        if current_day > 0:
            # Получаем количество дней в текущем месяце
            _, num_days = calendar.monthrange(current_year, current_month)

            # Проверяем, если текущий день больше количества дней в месяце
            if current_day > num_days:
                current_month += 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1
                current_day = 1

            button_text = str(current_day)
            callback_data = str(datetime(current_year, current_month, current_day))
            buttons.append(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )

            current_day += 1
    buttons.append(InlineKeyboardButton(text=lexicon["/abort"], callback_data="/abort"))
    kb_builder.row(*buttons, width=7)
    return kb_builder.as_markup()
