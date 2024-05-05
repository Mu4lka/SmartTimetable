import asyncio

from handlers import common, admin, worker, error
from loader import bot, dispatcher
from utils.methods import set_default_commands
from utils.methods.check_license import check_license
from utils.methods.on_startup_notify import on_startup_notify
from utils.background_tasks.notification_system.notify_admins import start_update_query, \
    start_notify_not_accepted_timetables
from utils.background_tasks.notification_system.notify_workers import start_update_timetable
from utils.background_tasks import start_copy_timetable


async def on_startup():
    await check_license()
    await set_default_commands(bot)
    await on_startup_notify()


async def main():
    await start_notify_not_accepted_timetables()
    await start_copy_timetable()
    await start_update_query()
    await start_update_timetable()
    await on_startup()
    dispatcher.include_routers(error.router, common.router, admin.router, worker.router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
