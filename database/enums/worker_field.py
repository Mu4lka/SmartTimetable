from enum import Enum


class WorkerField(str, Enum):
    ID = "id"
    FULL_NAME = "full_name"
    USER_NAME = "user_name"
    USER_ID = "user_id"
    KEY = "key"
    NUMBER_HOURS = "number_hours"
    NUMBER_WEEKEND = "number_weekend"
