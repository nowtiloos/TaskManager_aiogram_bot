import re

from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.db_interface import fetch_codes


# Фильтр проверки на верный код доступа к базе
class ValidatorCode(BaseFilter):
    def __init__(self) -> None:
        self.codes = fetch_codes()

    async def __call__(self, message: Message) -> bool:
        return message.text in self.codes


class ValidatorName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.[А-ЯЁ]\.$'
        match = re.match(pattern, message.text)
        return bool(match)
