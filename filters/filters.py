import re

from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.db_interface import query_database
from config_data import config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        admin_ids: list = config.tg_bot.admin_ids
        return message.from_user.id in admin_ids


# Фильтр проверки на верный код доступа к базе
class ValidatorCode(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # запрос к базе данных на предоставление всех code
        query: list = query_database(table="users", columns=("code",))
        # представление в виде списка
        rows: list[str] = [arg for rows in query for arg in rows]
        return message.text in rows


class Authorized(BaseFilter):
    async def __call__(self, message: Message) -> bool | None:
        tg_id = message.from_user.id
        # запрос значения auth по tg_id
        query: list = query_database(
            table="users", columns=("auth",), condition=f"tg_id = {tg_id}"
        )
        # распаковка значения поля auth
        if query:
            result, *_ = [arg for rows in query for arg in rows]
            return result


class ValidatorName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern = r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.[А-ЯЁ]\.$"
        match = re.match(pattern, message.text)
        return bool(match)
