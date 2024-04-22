from datetime import timedelta, date


def get_week_range(date: date, day: int = 7):
    first_day = date + timedelta(days=(day - date.weekday()))
    second_day = first_day + timedelta(days=6)
    return first_day, second_day
