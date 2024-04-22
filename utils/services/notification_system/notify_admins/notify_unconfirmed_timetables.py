import asyncio

from data import constants
from database import QueryType
from loader import query_table
from utils.methods.calculate_time_difference import UnitTime
from utils.methods import is_time_in_range, send_message_all_admins


async def notify_unconfirmed_timetables():
    while True:
        if len(await query_table.get_queries(QueryType.SENDING_TIMETABLE)) != 0:
            if is_time_in_range("12:00", "20:00"):
                await send_message_all_admins(
                    constants.NOTIFY_UNCONFIRMED_TIMETABLES
                )
            else:
                print("[INFO] Notification of new schedules was disabled due to time range!")
        await asyncio.sleep(30 * UnitTime.MINUTES.value)
