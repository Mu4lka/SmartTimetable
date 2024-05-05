from datetime import datetime, timedelta

from data import settings


def get_datetime_now():
    return datetime.now() + timedelta(hours=settings.TIMEZONE)
