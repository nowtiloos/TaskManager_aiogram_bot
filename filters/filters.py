import re

from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.db_interface import fetch_codes, auth_status
from config_data import config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        admin_ids: list = config.tg_bot.admin_ids
        return message.from_user.id in admin_ids


# Фильтр проверки на верный код доступа к базе
class ValidatorCode(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        codes = fetch_codes()  # Обновите список кодов при каждом вызове фильтра
        return message.text in codes


class Authorized(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return auth_status(message.from_user.id)


class ValidatorName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.[А-ЯЁ]\.$'
        match = re.match(pattern, message.text)
        return bool(match)
