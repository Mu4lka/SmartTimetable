from utils.methods import get_json_from_file
from utils.other import Week

config_file_path = "../data/settings.json"

settings_example = {
    "is_notify_start_up": False,
    "certain_days": [4, 5, 6],
    "worry_time": {"start": "12:00", "end": "20:00"},
    "not_accepted_timetables_day": 6,
    "timezone": 0
}

settings = get_json_from_file(config_file_path, settings_example)

IS_NOTIFY_START_UP = settings["is_notify_start_up"]
CERTAIN_DAYS = [Week(day) for day in settings["certain_days"]]
WORRY_TIME_START = settings["worry_time"]["start"]
WORRY_TIME_END = settings["worry_time"]["end"]
NOT_ACCEPTED_TIMETABLES_DAY = settings["not_accepted_timetables_day"]
TIMEZONE = settings["timezone"]
