from tabulate import tabulate

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from bot import bot
from db_interface import query_database


async def multi_delete(message: Message, count: int = 1):
    try:
        for step in range(count):
            await bot.delete_message(message.chat.id, message.message_id - step)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует),
        # код ошибки будет "Bad Request: message to delete not found"
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены")


def get_table():
    query = query_database(table='tasks', columns=('task_id', 'task_text'))
    headers = ['id', 'text']
    table = tabulate(query, headers, tablefmt='grid')
    return table
