from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import Message
from lexicon import lexicon
from services.db_interface import update_auth

# Инициализируем роутер уровня модуля
router = Router()


@router.message(Command(commands="quit"))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text="quitting")
    await update_auth(tg_id=message.from_user.id, value=0)
    await state.clear()


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=lexicon["/help"])


#
# # Хэндлер для сообщений, которые не попали в другие хэндлеры
# @router.message()
# async def send_answer(message: Message):
#     await message.answer(text=lexicon['other_answer'])
