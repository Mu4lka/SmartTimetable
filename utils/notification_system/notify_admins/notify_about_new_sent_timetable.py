import asyncio
from datetime import datetime, time

from data import constants
from data.config import ADMIN_IDS
from loader import bot, query_table
from utils.methods.calculate_time_difference import UnitTime


async def notify_about_new_sent_timetable():
    while True:
        if (len(await query_table.get_queries()) != 0 and
                is_time_in_range("12:00", "23:30")):
            for admin_id in ADMIN_IDS:
                await bot.send_message(
                    admin_id,
                    constants.NOTIFY_ABOUT_NEW_SENT_TIMETABLE
                )
        await asyncio.sleep(30 * UnitTime.MINUTES.value)


def is_time_in_range(start: str, end: str, check_time: time = None):
    if check_time is None:
        check_time = datetime.now().time()

    start = time.fromisoformat(start)
    end = time.fromisoformat(end)

    if start <= check_time <= end:
        return True

    return start > end and (check_time >= start or check_time <= end)
