import asyncio
from datetime import datetime, timedelta

from database import WorkerField
from utils.other import Week
from loader import worker_table
from utils.methods import send_message_all_admins
from utils.methods.calculate_time_difference import UnitTime

accepted_full_names = set()


async def notify_not_accepted_timetables():
    while True:
        if check_current_time(Week.FRIDAY.value, "20:00"):
            result = await worker_table.select(
                columns=[WorkerField.FULL_NAME.value]
            )
            not_accepted_full_names = []
            for item in result:
                full_name = item[0]
                if full_name not in accepted_full_names:
                    not_accepted_full_names.append(full_name)
            accepted_full_names.clear()
            if len(not_accepted_full_names) > 0:
                await send_message_all_admins(
                    f"Сотрудники, у которых не изменилось расписание "
                    f"на следующую неделю: {', '.join(not_accepted_full_names)}"
                )
        await asyncio.sleep(UnitTime.HOURS.value)


def check_current_time(day_of_week: int, time_to_check: str):
    current_day_of_week = datetime.now().weekday()
    current_time = datetime.now()
    hour, minute = map(int, time_to_check.split(':'))
    time_to_check = current_time.replace(hour=hour, minute=minute)
    delta = timedelta(hours=1)
    return (current_day_of_week == day_of_week and
            (time_to_check - delta) <= current_time <= (time_to_check + delta))
