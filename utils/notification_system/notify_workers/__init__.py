import asyncio

from loader import timetable_storage
from .notify_change import notify_change
from .notify_shift_starts import notify_shift_starts


async def start_update_timetable():
    timetable_storage.on_update.subscribe(notify_shift_starts)
    timetable_storage.on_change.subscribe(notify_change)
    task = asyncio.create_task(timetable_storage.start_update())
