import asyncio
from datetime import timedelta

from data.settings import WORRY_TIME_END, NOT_ACCEPTED_TIMETABLES_DAY
from database import WorkerField
from loader import worker_table
from utils.methods import send_message_all_admins
from utils.methods.calculate_time_difference import UnitTime
from utils.methods.get_datetime_now import get_datetime_now

accepted_full_names = set()


async def notify_not_accepted_timetables():
    while True:
        if check_current_time(
                NOT_ACCEPTED_TIMETABLES_DAY, WORRY_TIME_END):
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
                message_full_names = '\n'.join(not_accepted_full_names)
                await send_message_all_admins(
                    f"<b>Сотрудники, у которых не изменилось расписание "
                    f"на следующую неделю:</b>\n{message_full_names}"
                )
        await asyncio.sleep(UnitTime.HOURS.value)


def check_current_time(day_of_week: int, time_to_check: str):
    current_time = get_datetime_now()
    current_day_of_week = current_time.weekday()
    hour, minute = map(int, time_to_check.split(':'))
    time_to_check = current_time.replace(hour=hour, minute=minute)
    delta = timedelta(hours=1)
    return (current_day_of_week == day_of_week and
            (time_to_check - delta) <= current_time <= (time_to_check + delta))
