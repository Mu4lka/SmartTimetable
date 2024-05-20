from datetime import datetime, time, timedelta, date
from typing import Union

import data


def get_datetime_now():
    return datetime.now() + timedelta(hours=data.settings.TIMEZONE)


def check_current_time(day_of_week: int, time_to_check: str):
    current_time = get_datetime_now()
    current_day_of_week = current_time.weekday()
    hour_to_check = time_to_check.split(':')[0]
    current_hour = current_time.time().hour
    return (current_day_of_week == day_of_week
            and current_hour == int(hour_to_check))


def get_week_range(date: date, day: int = 7):
    first_day = date + timedelta(days=(day - date.weekday()))
    second_day = first_day + timedelta(days=6)
    return first_day, second_day


class TimeRange:
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end

    def time_is_in_range(self, check_time: Union[str, time]):
        if isinstance(check_time, str):
            check_time = datetime.strptime(check_time, "%H:%M").time()
        start = time.fromisoformat(self.start)
        end = time.fromisoformat(self.end)

        if start <= check_time <= end:
            return True

        return start > end and (check_time >= start or check_time <= end)

    def difference_in_second(self):
        start = datetime.strptime(self.start, "%H:%M")
        if self.end == "24:00":
            end = datetime.combine(
                start.date() + timedelta(days=1), datetime.min.time()
            )
        else:
            end = datetime.strptime(
                self.end, "%H:%M"
            )
        if start > end:
            end += timedelta(days=1)

        shift_duration = end - start
        return shift_duration.total_seconds()
