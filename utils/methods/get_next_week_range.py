from datetime import timedelta, date, datetime


def get_next_week_range(date: date):
    next_monday = date + timedelta(days=(7 - date.weekday()))
    next_sunday = next_monday + timedelta(days=6)
    return next_monday, next_sunday


def get_name_for_sheet_on_next_week():
    next_monday, next_sunday = get_next_week_range(datetime.now().date())
    return f"{next_monday.strftime('%d.%m')}-{next_sunday.strftime('%d.%m')}"
