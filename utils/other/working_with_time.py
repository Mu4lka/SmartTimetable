from datetime import datetime, time, timedelta
from typing import Union


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
