from datetime import timedelta, date


def get_week_range(date: date, day: int = 7):
    next_monday = date + timedelta(days=(day - date.weekday()))
    next_sunday = next_monday + timedelta(days=6)
    return next_monday, next_sunday

