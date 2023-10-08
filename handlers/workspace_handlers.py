from aiogram import Router, Bot
from aiogram.filters import StateFilter, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram import F

from fsm.fsm import FSMEntry
from keyboards.inline_keyboard import buttons, name_button, create_inline_kb


router = Router()
# Хэндлеры работают если выполнен вход
router.message.filter(StateFilter(FSMEntry.successful_entry))


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    keyboard = create_inline_kb(2, 'button', 'cott', 'sdf')

    await message.answer(text='workspace', reply_markup=keyboard)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed'
@router.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Была нажата БОЛЬШАЯ КНОПКА 1',
        reply_markup=callback.message.reply_markup
    )


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_2_pressed'
@router.callback_query(F.data == 'big_button_2_pressed')
async def process_button_2_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Была нажата БОЛЬШАЯ КНОПКА 2',
        reply_markup=callback.message.reply_markup
    )
