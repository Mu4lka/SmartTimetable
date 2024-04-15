import asyncio

from utils.tasks.copy_sheet_for_next_week import copy_sheet_for_next_week


async def start_copy_sheet_for_next_week():
    task = asyncio.create_task(copy_sheet_for_next_week())
