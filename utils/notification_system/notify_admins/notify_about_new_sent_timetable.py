import asyncio

from UI.buttons.enums.main_menu import AdminButton
from data.config import ADMIN_IDS
from handlers.admin.coordinate_timetables import get_queries
from loader import bot


async def notify_about_new_sent_timetable():
    while True:
        if len(await get_queries()) != 0:
            for admin_id in ADMIN_IDS:
                await bot.send_message(
                    admin_id,
                    "Есть расписания, которые отправили сотрудники! "
                    f"Нажмите в главном меню кнопку \"{AdminButton.COORDINATE_TIMETABLES.value}\", "
                    f"чтобы их принять или отклонить")
        await asyncio.sleep(30 * 60)
