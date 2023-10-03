from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from keyboards.standart_keyboard import start_kb, register_kb
from services.access import get_access

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=start_kb)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер срабатывает на кнопку "Регистрация"
@router.message(F.text == LEXICON_RU['register'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['input_reg'], reply_markup=register_kb)


# Этот хэндлер срабатывает на кнопку "Вход"
@router.message(F.text == LEXICON_RU['sign_in'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['input_uid'])


# Этот хэндлер срабатывает на кнопку "Мастер-приемщик"
@router.message(F.text == LEXICON_RU['manager'])
async def process_yes_answer(message: Message):
    uid = get_access(LEXICON_RU['manager'])
    await message.answer(text=uid)


# Этот хэндлер срабатывает на кнопку "Мастер рем-зоны"
@router.message(F.text == LEXICON_RU['master'])
async def process_yes_answer(message: Message):
    uid = get_access(LEXICON_RU['master'])
    await message.answer(text=uid)


# Этот хэндлер срабатывает на кнопку "Электрик-диагност"
@router.message(F.text == LEXICON_RU['staff'])
async def process_yes_answer(message: Message):
    uid = get_access(LEXICON_RU['staff'])
    await message.answer(text=uid)
