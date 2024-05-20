import asyncio

from data import settings, save
from database import WorkerField
from loader import worker_table
from utils.methods import send_message_all_admins
from utils.other.working_with_time import check_current_time


async def get_not_accepted_full_names():
    result = await worker_table.select(
        columns=[WorkerField.FULL_NAME.value]
    )
    not_accepted_full_names = []
    for item in result:
        full_name = item[0]
        if full_name not in save.ACCEPTED_FULL_NAMES:
            not_accepted_full_names.append(full_name)
    return not_accepted_full_names


async def notify_not_accepted_timetables():
    while True:
        if check_current_time(
                settings.NOT_ACCEPTED_TIMETABLES_DAY,
                settings.get_alert_time().end):
            not_accepted_full_names = await get_not_accepted_full_names()

            if len(not_accepted_full_names) == 0:
                break

            message_full_names = '\n'.join(not_accepted_full_names)
            await send_message_all_admins(
                f"<b>Сотрудники, у которых не изменилось расписание "
                f"на следующую неделю:</b>\n{message_full_names}"
            )
            save.ACCEPTED_FULL_NAMES.clear()
            save.unload()
        await asyncio.sleep(3600)
