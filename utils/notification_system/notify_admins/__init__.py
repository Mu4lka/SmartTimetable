import asyncio

from .notify_about_new_sent_timetable import notify_about_new_sent_timetable


async def start_update_query():
    task = asyncio.create_task(notify_about_new_sent_timetable())
