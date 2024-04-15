import asyncio

from aiogram import Bot

from database.methods import create_database
from handlers import common, admin, worker, error
from loader import bot, dispatcher
from utils.methods import set_default_commands
from utils.notification_system.notify_admins import start_update_query
from utils.notification_system.notify_admins.on_startup_notify import on_startup_notify
from utils.notification_system.notify_workers import start_update_timetable
from utils.tasks import start_copy_sheet_for_next_week


async def on_startup(bot: Bot):
    await set_default_commands(bot)
    await on_startup_notify(bot)


async def main():
    await start_copy_sheet_for_next_week()
    await start_update_query()
    await start_update_timetable()
    await create_database()
    await on_startup(bot)
    dispatcher.include_routers(error.router, common.router, admin.router, worker.router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
