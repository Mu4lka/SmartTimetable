from datetime import datetime

from database import WorkerField
from loader import bot, worker_table
from utils.methods import calculate_time_difference
from utils.methods.calculate_time_difference import UnitTime


async def get_shift_starts(timetable: list, workers: dict):
    weekday = datetime.now().weekday()
    shift_starts = {}
    for row in timetable:
        try:
            shift = row[weekday + 1]
            shift_start = shift.split("-", 1)[0]
            datetime.strptime(shift_start, "%H:%M")
            shift_starts.update({workers[row[0]]: shift_start})
        except Exception:
            pass
    return shift_starts


def check_time_until_shift_start(shift_start: str, minutes_threshold=15):
    if minutes_threshold < 0:
        raise ValueError("Invalid minute value. The value cannot be negative")

    time_difference = calculate_time_difference(
        datetime.now().strftime("%H:%M"),
        shift_start,
        UnitTime.MINUTES)
    return time_difference == minutes_threshold


async def notify_shift_starts(timetable: list, minutes_threshold=15):
    workers = await worker_table.get_authorized(
        [WorkerField.FULL_NAME.value, WorkerField.TELEGRAM_ID.value]
    )
    shift_starts = await get_shift_starts(timetable, workers)
    for worker_id, shift_start in shift_starts.items():
        if check_time_until_shift_start(shift_start, minutes_threshold):
            await bot.send_message(
                worker_id, f"Ваша смена начнется в {shift_start}!"
            )
