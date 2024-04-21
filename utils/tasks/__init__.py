import asyncio

from utils.tasks.copy_timetable_to_specific_days import copy_timetable_to_specific_days


async def start_copy_sheet_for_next_week():
    task = asyncio.create_task(copy_timetable_to_specific_days())
