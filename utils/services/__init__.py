import asyncio

from utils.services.copy_timetable_to_specific_days import copy_timetable_to_specific_days


async def start_copy_timetable():
    task = asyncio.create_task(copy_timetable_to_specific_days())
