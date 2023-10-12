import re

from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.db_interface import fetch_users_db, auth_status


# Фильтр проверки на верный код доступа к базе
class ValidatorCode(BaseFilter):
    def __init__(self) -> None:
        self.codes = fetch_users_db('code')

    async def __call__(self, message: Message) -> bool:
        return message.text in self.codes


class Authorized(BaseFilter):
    def __init__(self) -> None:
        self.auth = auth_status

    async def __call__(self, message: Message) -> bool:
        return self.auth(message.from_user.id)


class ValidatorName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.[А-ЯЁ]\.$'
        match = re.match(pattern, message.text)
        return bool(match)
