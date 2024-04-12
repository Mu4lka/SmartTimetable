import asyncio

from loader import timetable
from .notify_change import notify_change
from .notify_shift_starts import notify_shift_starts


async def start_update_timetable():
    timetable.on_update.subscribe(notify_shift_starts)
    timetable.on_change.subscribe(notify_change)
    task = asyncio.create_task(timetable.start_update())
