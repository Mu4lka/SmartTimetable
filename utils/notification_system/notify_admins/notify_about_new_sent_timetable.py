import asyncio
from datetime import datetime, time

from data import constants
from data.config import ADMIN_IDS
from database import QueryType
from loader import bot, query_table
from utils.methods.calculate_time_difference import UnitTime
from utils.methods import is_time_in_range


async def notify_about_new_sent_timetable():
    while True:
        if len(await query_table.get_queries(QueryType.SENDING_TIMETABLE)) != 0:
            if is_time_in_range("12:00", "20:00"):
                for admin_id in ADMIN_IDS:
                    await bot.send_message(
                        admin_id,
                        constants.NOTIFY_ABOUT_NEW_SENT_TIMETABLE
                    )
            else:
                print("[INFO] Notification of new schedules was disabled due to time range!")
        await asyncio.sleep(30 * UnitTime.MINUTES.value)
