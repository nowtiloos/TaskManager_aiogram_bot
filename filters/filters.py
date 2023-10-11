import re

from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.db_interface import fetch_users_db


# Фильтр проверки на верный код доступа к базе
class ValidatorCode(BaseFilter):
    def __init__(self) -> None:
        self.codes = fetch_users_db('code')

    async def __call__(self, message: Message) -> bool:
        return message.text in self.codes


class ValidatorID(BaseFilter):
    def __init__(self) -> None:
        self.ids = fetch_users_db('tg_id')

    async def __call__(self, message: Message) -> bool:
        return int(message.from_user.id) in self.ids


class ValidatorName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.[А-ЯЁ]\.$'
        match = re.match(pattern, message.text)
        return bool(match)
