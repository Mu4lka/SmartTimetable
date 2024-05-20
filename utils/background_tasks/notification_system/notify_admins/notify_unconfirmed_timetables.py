import asyncio

from data import constants, settings
from database import QueryType
from loader import query_table
from utils.methods import send_message_all_admins
from utils.other.working_with_time import get_datetime_now


async def notify_unconfirmed_timetables():
    while True:
        if len(await query_table.get_queries(QueryType.SENDING_TIMETABLE)) != 0:
            alert_time = settings.get_alert_time()

            if alert_time.time_is_in_range(get_datetime_now().time()):
                await send_message_all_admins(
                    constants.NOTIFY_UNCONFIRMED_TIMETABLES
                )
            else:
                print("[INFO] Notification of new schedules was disabled due to time range!")
        await asyncio.sleep(30 * 60)
