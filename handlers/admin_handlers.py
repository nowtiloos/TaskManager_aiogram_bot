from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.db_interface import clear_table
from filters import IsAdmin

router = Router()
router.message.filter(IsAdmin())


@router.message(Command(commands='clear_users'))
async def process_clear_users_table(message: Message):
    await message.answer(text='Users table clear')
    await clear_table(table='users')


@router.message(Command(commands='clear_tasks'))
async def process_clear_tasks_table(message: Message):
    await message.answer(text='Users table clear')
    await clear_table(table='tasks')
