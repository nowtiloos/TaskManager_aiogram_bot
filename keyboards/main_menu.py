from aiogram import Bot
from aiogram.types import BotCommand

from lexicon import lexicon


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description=lexicon["/start"]),
        BotCommand(command="/help", description=lexicon["/help"]),
        BotCommand(command="/quit", description=lexicon["/quit"]),
        BotCommand(command="/clear_users", description="clear users table"),
    ]
    await bot.set_my_commands(main_menu_commands)
