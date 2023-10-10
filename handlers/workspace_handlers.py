from aiogram import Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram import F

from fsm.fsm import FSMEntry
from keyboards.inline_keyboard import keyboard
from lexicon.lexicon import LEXICON_RU

router = Router()
# Хэндлеры работают если выполнен вход
router.message.filter(StateFilter(FSMEntry.successful_entry))


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['welcome'], reply_markup=keyboard)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
@router.callback_query(F.data == 'add_task_pressed')
async def process_add_task_press(callback: CallbackQuery):
    await callback.message.answer(
        text='Добавьте задачи в список',
        reply_markup=mark)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
@router.callback_query(F.data == 'show_tasks_today_pressed')
async def process_show_tasks_today_press(callback: CallbackQuery):
    await callback.message.answer(text='Список задач на сегодня')
