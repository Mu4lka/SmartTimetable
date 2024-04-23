from utils.methods import get_json_from_file
from utils.other import Week

config_file_name = "settings.json"

settings_example = {
    "certain_days": [4, 5, 6],
    "worry_time": {"start": "12:00", "end": "20:00"},
    "not_accepted_timetables_day": 6
}

settings = get_json_from_file(config_file_name, settings_example)

CERTAIN_DAYS = [Week(day) for day in settings["certain_days"]]
WORRY_TIME_START = settings["worry_time"]["start"]
WORRY_TIME_END = settings["worry_time"]["end"]
NOT_ACCEPTED_TIMETABLES_DAY = settings["not_accepted_timetables_day"]
