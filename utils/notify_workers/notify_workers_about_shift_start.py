from datetime import datetime

from loader import bot

minutes_before_shift_start = 15


def check_time_until_shift_start(shift_start: str, minutes_threshold=15):
    if minutes_threshold < 0:
        raise ValueError("Invalid minute value. The value cannot be negative")

    format = "%H:%M"
    current_time = datetime.strptime(datetime.now().strftime(format), format)
    shift_start_time = datetime.strptime(shift_start, format)
    time_until_shift_start = shift_start_time - current_time
    minutes_until_shift_start = time_until_shift_start.total_seconds() / 60
    if minutes_until_shift_start == minutes_threshold:
        return True
    else:
        return False


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


async def notify_about_shift_start(timetable: list, workers: dict):
    shift_starts = await get_shift_starts(timetable, workers)
    for worker_id, shift_start in shift_starts.items():
        if check_time_until_shift_start(shift_start, minutes_before_shift_start):
            await send_shift_start_message(worker_id)


async def send_shift_start_message(worker_id):
    message_text = f"Ваша смена начнется через {minutes_before_shift_start} минут!"
    await bot.send_message(worker_id, message_text)
