from enum import Enum


class WorkerField(str, Enum):
    ID = "id"
    FULL_NAME = "full_name"
    USER_NAME = "user_name"
    ID_TELEGRAM = "id_telegram"
    KEY = "key"
    NUMBER_HOURS = "number_hours"
    NUMBER_WEEKEND = "number_weekend"
