from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

# ------- Создаем клавиатуру регистрации и входа -------

# Создаем кнопки с ответами регистрации и входа
button_register = KeyboardButton(text=LEXICON_RU['register'])
button_sign_in = KeyboardButton(text=LEXICON_RU['sign_in'])

# Инициализируем билдер для клавиатуры с кнопками "Регистрация" и "Вход"
reg_signin_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
reg_signin_builder.row(button_register, button_sign_in, width=2)

# Создаем клавиатуру с кнопками "Регистрация" и "Вход"
start_kb: ReplyKeyboardMarkup = reg_signin_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)

# -----------------------------------------------------

# ------- Создаем клавиатуру регистрации uid ----------

# Создаем кнопки с ответами регистрации uid
button_manger = KeyboardButton(text=LEXICON_RU['manager'])
button_master = KeyboardButton(text=LEXICON_RU['master'])
button_staff = KeyboardButton(text=LEXICON_RU['staff'])
button_cancel = KeyboardButton(text=LEXICON_RU['/cancel'])

# Инициализируем билдер для клавиатуры с кнопками регистрации uid
reg_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
reg_builder.row(button_manger, button_master, button_staff, button_cancel, width=2)

# Создаем клавиатуру с кнопками "Регистрация" и "Вход"
register_kb: ReplyKeyboardMarkup = reg_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)




