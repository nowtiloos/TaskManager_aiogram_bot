from aiogram.filters import BaseFilter
from aiogram.types import Message
from databases.users_db import user_dict


# Фильтр проверки на верный код доступа к базе
class Validator(BaseFilter):
    def __init__(self) -> None:
        self.database = user_dict

    async def __call__(self, message: Message) -> bool:
        return message.text in self.database
