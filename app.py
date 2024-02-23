import asyncio

from aiogram import Bot, Router

from database.create_database import create_database
from handlers import common
from handlers.admin import create_worker, show_workers, generate_timetable
from handlers.worker import swap_shifts, select_weekend, show_my_timetable
from loader import dispatcher, bot
from utils.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify


async def on_startup(bot: Bot):
    await set_default_commands(bot)
    await on_startup_notify(bot)


def include_routers():
    admin_routers = Router()
    admin_routers.include_routers(
        create_worker.router,
        show_workers.router,
        generate_timetable.router
    )
    worker_routers = Router()
    worker_routers.include_routers(
        swap_shifts.router,
        select_weekend.router,
        show_my_timetable.router
    )
    dispatcher.include_routers(common.router, admin_routers, worker_routers)


async def main():
    create_database()
    await on_startup(bot)
    include_routers()
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
