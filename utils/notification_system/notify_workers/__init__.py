import asyncio

from loader import storage_timetable
from .notify_change import notify_change
from .notify_shift_starts import notify_shift_starts


async def start_update_timetable():
    storage_timetable.on_update.subscribe(notify_shift_starts)
    storage_timetable.on_change.subscribe(notify_change)
    task = asyncio.create_task(storage_timetable.start_update())
