from enum import Enum

from utils.ease_sql import Table, Database


class ErrorField(str, Enum):
    ID = "id"
    TIME = "time"
    JSON = "json"
    TEXT = "text"


class ErrorTable(Table):
    name = "Errors"
    fields = (f"{ErrorField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,"
              f"{ErrorField.TIME.value} TEXT,"
              f"{ErrorField.TEXT.value} TEXT,"
              f"{ErrorField.JSON.value} TEXT")

    def __init__(self, database: Database):
        super().__init__(self.name, database, self.fields)
