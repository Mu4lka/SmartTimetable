from utils.other import JsonFile, TimeRange


class Save(JsonFile):
    def __init__(self, path: str):
        self.ACCEPTED_FULL_NAMES = []
        super().__init__(path)


class Settings(JsonFile):
    def __init__(self, path: str):
        self.IS_NOTIFY_START_UP = False
        self.CERTAIN_DAYS = [4, 5, 6]
        self.ALERT_TIME = vars(TimeRange("12:00", "20:00"))
        self.NOT_ACCEPTED_TIMETABLES_DAY = 6
        self.TIMEZONE = 0
        super().__init__(path)

    def get_alert_time(self):
        start = self.ALERT_TIME["start"]
        end = self.ALERT_TIME["end"]
        return TimeRange(start, end)


class Config(JsonFile):
    def __init__(self, path: str):
        self.BOT_TOKEN = "bot token"
        self.ADMIN_IDS = [1000000000, 1111111111]
        self.LINK_TO_TIMETABLE = "link to timetable"
        self.CREDENTIALS_FILE = "name of the service account login credentials file"
        self.SPREADSHEET_ID = "spreadsheet id to timetable"
        super().__init__(path)
