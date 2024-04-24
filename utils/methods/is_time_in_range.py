from datetime import datetime, time

from utils.methods.get_datetime_now import get_datetime_now


def is_time_in_range(start: str, end: str, check_time: str = None):
    if check_time is None:
        check_time = get_datetime_now().time()
    else:
        check_time = datetime.strptime(check_time, "%H:%M").time()
    start = time.fromisoformat(start)
    end = time.fromisoformat(end)

    if start <= check_time <= end:
        return True

    return start > end and (check_time >= start or check_time <= end)
