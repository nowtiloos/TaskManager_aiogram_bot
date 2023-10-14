from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_RU


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description=LEXICON_RU['/start']),
        BotCommand(command='/help',
                   description=LEXICON_RU['/help']),
        BotCommand(command='/quit',
                   description=LEXICON_RU['/quit']),
        BotCommand(command='/clear_users',
                   description='clear users table')

    ]
    await bot.set_my_commands(main_menu_commands)
