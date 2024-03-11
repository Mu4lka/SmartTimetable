from enum import Enum


class QueryField(str, Enum):
    ID = "query_id"
    WORKER_ID = "worker_id"
    TYPE = "query_type"
    QUERY_TEXT = "query_text"


class QueryType(str, Enum):
    SENDING_TIMETABLE = "sending_timetable"
    CHANGING_SHIFT = "changing_shift"
