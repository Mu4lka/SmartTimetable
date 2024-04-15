from datetime import datetime, timedelta
from enum import Enum


class UnitTime(int, Enum):
    SECONDS = 1
    MINUTES = 60
    HOURS = 3600


def calculate_time_difference(first_time_str: str, second_time_str: str, unit_time: UnitTime, format: str = "%H:%M"):
    first_time = datetime.strptime(first_time_str, format)
    if second_time_str == "24:00":
        second_time = datetime.combine(first_time.date() + timedelta(days=1), datetime.min.time())
    else:
        second_time = datetime.strptime(second_time_str, format)
    if first_time > second_time:
        second_time += timedelta(days=1)

    shift_duration = second_time - first_time
    return shift_duration.total_seconds() / unit_time.value
