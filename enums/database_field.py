from enum import Enum


class DatabaseField(str, Enum):
    ID = "id"
    NAME = "name"
    USER_NAME = "user_name"
    ID_TELEGRAM = "id_telegram"
    KEY = "key"
    SHIFT_DURATION = "shift_duration"
    EARLY_SHIFT_START = "early_shift_start"
    LATE_SHIFT_START = "late_shift_start"
    EFFICIENCY = "efficiency"
    WEEKEND = "weekend"
    POSSIBLE_WEEKEND = "possible_weekend"
    PRIORITY = "priority"
