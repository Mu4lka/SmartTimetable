import asyncio

from aiogram import Bot

from database.methods import create_database
from handlers import common, admin, worker, error
from loader import bot, dispatcher
from utils.methods import set_default_commands, on_startup_notify
from utils.notify_workers import start_update_timetable


async def on_startup(bot: Bot):
    await set_default_commands(bot)
    await on_startup_notify(bot)


async def main():
    await start_update_timetable()
    await create_database()
    await on_startup(bot)
    dispatcher.include_routers(error.router, common.router, admin.router, worker.router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
