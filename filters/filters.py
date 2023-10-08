from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.db import fetch_codes


# Фильтр проверки на верный код доступа к базе
class Validator(BaseFilter):
    def __init__(self) -> None:
        self.codes = fetch_codes()

    async def __call__(self, message: Message) -> bool:
        return message.text in self.codes
