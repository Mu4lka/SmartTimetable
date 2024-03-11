from enum import Enum


class WorkerField(str, Enum):
    ID = "worker_id"
    FULL_NAME = "full_name"
    USER_NAME = "user_name"
    TELEGRAM_ID = "telegram_id"
    KEY = "key"
    NUMBER_HOURS = "number_hours"
    NUMBER_WEEKEND = "number_weekend"
