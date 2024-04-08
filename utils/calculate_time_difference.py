from datetime import datetime
from enum import Enum


class UnitTime(int, Enum):
    SECONDS = 1
    MINUTES = 60
    HOURS = 3600


def calculate_time_difference(first_time: str, second_time: str, unit_time: UnitTime, format: str = "%H:%M"):
    first_time = datetime.strptime(first_time, format)
    second_time = datetime.strptime(second_time, format)
    shift_duration = second_time - first_time
    return shift_duration.total_seconds() / unit_time.value
