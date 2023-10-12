import uuid

from aiogram.exceptions import TelegramBadRequest

from bot import bot

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline_keyboard import create_inline_kb
from lexicon.lexicon import LEXICON_RU
from services.db_interface import insert


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
async def to_user_database(callback: CallbackQuery, state: FSMContext, code: str):
    await callback.message.edit_text(text=f'Ваш код доступа к базе: {code}')
    await state.update_data(role=LEXICON_RU['staff'])
    await state.update_data(code=code)
    # Добавляем в "базу данных" анкету пользователя
    insert(table='users', data_dict=await state.get_data())
    await state.clear()
    markup = create_inline_kb('register', 'sign_in')
    await callback.message.answer(text=LEXICON_RU['final_reg'], reply_markup=markup)


async def multi_delete(message: Message, count: int = 1):
    try:
        for step in range(count):
            await bot.delete_message(message.chat.id, message.message_id - step)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует),
        # код ошибки будет "Bad Request: message to delete not found"
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены")
