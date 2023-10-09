import uuid

from aiogram.exceptions import TelegramBadRequest

from bot import bot

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.standart_keyboard import start_kb
from lexicon.lexicon import LEXICON_RU
from services.db_interface import insert_data_from_dict


# Функция генерации ключа доступа к базе задач
def get_access(unit: str) -> str | None:
    code = None
    match unit:
        case 'manager':
            code = uuid.uuid4().hex
        case 'master':
            code = uuid.uuid4().hex
        case 'staff':
            code = uuid.uuid4().hex
    return code


# Функция забирает данные из Redis и передает их в БД
async def to_database(message: Message, state: FSMContext, code: str):
    await message.answer(text=f'Ваш код доступа к базе: {code}')
    await state.update_data(role=LEXICON_RU['staff'])
    await state.update_data(code=code)
    # Добавляем в "базу данных" анкету пользователя
    insert_data_from_dict(await state.get_data())
    await state.clear()
    await message.answer(text=LEXICON_RU['final_reg'], reply_markup=start_kb)


async def multi_delete(message: Message, count: int = 1):
    try:
        for step in range(count):
            await bot.delete_message(message.chat.id, message.message_id - step)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует),
        # код ошибки будет "Bad Request: message to delete not found"
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены")
