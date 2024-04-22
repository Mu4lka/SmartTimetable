import asyncio

from .notify_not_accepted_timetables import notify_not_accepted_timetables
from .notify_unconfirmed_timetables import notify_unconfirmed_timetables


async def start_update_query():
    task = asyncio.create_task(notify_unconfirmed_timetables())


async def start_notify_not_accepted_timetables():
    task = asyncio.create_task(notify_not_accepted_timetables())
