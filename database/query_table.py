from enum import Enum

from database.worker_table import WorkerTable, WorkerField
from utils.ease_sql import Table, Database


class QueryField(str, Enum):
    ID = "query_id"
    WORKER_ID = "worker_id"
    TYPE = "query_type"
    QUERY_TEXT = "query_text"


class QueryType(str, Enum):
    SENDING_TIMETABLE = "sending_timetable"
    CHANGING_SHIFT = "changing_shift"


class QueryTable(Table):
    name = "Queries"
    fields = (f"{QueryField.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT,"
              f"{QueryField.WORKER_ID.value} INTEGER,"
              f"{QueryField.TYPE.value} TEXT,"
              f"{QueryField.QUERY_TEXT.value} TEXT,"
              f"FOREIGN KEY ({QueryField.WORKER_ID.value})"
              f"REFERENCES {WorkerTable.name}({WorkerField.ID.value})")

    def __init__(self, database: Database):
        super().__init__(self.name, database, self.fields)

    async def get_queries(self, query_type: QueryType):
        return await self.select(
            f"{QueryField.TYPE.value} = ?",
            (query_type.value,)
        )
