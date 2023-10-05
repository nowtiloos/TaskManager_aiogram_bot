import uuid

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from databases.users_db import user_dict
from lexicon.lexicon import LEXICON_RU


# Функция генерации ключа доступа к базе задач
def get_access(unit: str) -> str:
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
    await state.update_data(code=code)
    await state.update_data(role=LEXICON_RU['staff'])
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
