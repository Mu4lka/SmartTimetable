from datetime import datetime

from database.methods import get_authorized_workers
from loader import bot
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

    return calculate_time_difference(
        datetime.now().strftime("%H:%M"),
        shift_start,
        UnitTime.MINUTES) == minutes_threshold


async def notify_shift_starts(timetable: list, minutes_threshold=15):
    workers = await get_authorized_workers()
    shift_starts = await get_shift_starts(timetable, workers)
    for worker_id, shift_start in shift_starts.items():
        if check_time_until_shift_start(shift_start, minutes_threshold):
            await bot.send_message(
                worker_id,
                f"Ваша смена начнется через {minutes_threshold} минут!"
            )
