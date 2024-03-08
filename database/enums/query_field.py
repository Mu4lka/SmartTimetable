from enum import Enum


class QueryField(str, Enum):
    ID = "id"
    USER_ID = "user_id"
    TYPE = "type"
    QUERY_TEXT = "query_text"


class QueryType(str, Enum):
    MAKING_TIMETABLE_BY_WORKER = "making_timetable_by_worker"
