import asyncio

from aiogram import Bot

from database.create_database import create_database
from handlers import common, admin, worker
from loader import bot, dispatcher
from utils import set_default_commands, on_startup_notify


async def on_startup(bot: Bot):
    await set_default_commands(bot)
    await on_startup_notify(bot)


async def main():
    create_database()
    await on_startup(bot)
    dispatcher.include_routers(common.router, admin.router, worker.router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
