from datetime import timedelta, date, datetime


def get_week_range(date: date, day: int = 7):
    next_monday = date + timedelta(days=(day - date.weekday()))
    next_sunday = next_monday + timedelta(days=6)
    return next_monday, next_sunday


def get_sheet_name(day: int = 7):
    next_monday, next_sunday = get_week_range(datetime.now().date(), day)
    return f"{next_monday.strftime('%d.%m')}-{next_sunday.strftime('%d.%m')}"
