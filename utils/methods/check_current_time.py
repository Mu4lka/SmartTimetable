from utils.methods.get_datetime_now import get_datetime_now


def check_current_time(day_of_week: int, time_to_check: str):
    current_time = get_datetime_now()
    current_day_of_week = current_time.weekday()
    hour_to_check = time_to_check.split(':')[0]
    current_hour = current_time.time().hour
    return (current_day_of_week == day_of_week
            and current_hour == int(hour_to_check))
