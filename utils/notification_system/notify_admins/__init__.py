import asyncio

from .new_sent_timetables import new_sent_timetables


async def start_update_query():
    task = asyncio.create_task(new_sent_timetables())
