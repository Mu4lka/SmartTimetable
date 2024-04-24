from datetime import datetime, timedelta

from data.settings import TIMEZONE


def get_datetime_now():
    return datetime.now() + timedelta(hours=TIMEZONE)
