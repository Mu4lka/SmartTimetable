import asyncio

from database.database_config import table_workers, database_name
from database.enums import WorkerField
from google_sheets.methods import get_timetable
from utils import sql
from utils.google_sheets.enums import Dimension
from utils.notify_workers.notify_workers_about_changes import notify_about_changes_in_timetable
from utils.notify_workers.notify_workers_about_shift_start import notify_about_shift_start


async def get_workers():
    result = await sql.select(
        database_name,
        table_workers,
        f"{WorkerField.TELEGRAM_ID.value} IS NOT NULL", (),
        columns=[WorkerField.FULL_NAME.value, WorkerField.TELEGRAM_ID.value]
    )
    return dict(result)


async def notify_workers():
    timetable = None
    while True:
        try:
            current_timetable = await get_timetable(Dimension.ROWS)
            workers = await get_workers()
            await notify_about_changes_in_timetable(timetable, current_timetable, workers)
            await notify_about_shift_start(current_timetable, workers)
            timetable = current_timetable
        except Exception:
            await asyncio.sleep(1)
            continue
        await asyncio.sleep(60)


async def start_notify_workers():
    task = asyncio.create_task(notify_workers())
