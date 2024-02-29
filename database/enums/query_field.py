from enum import Enum


class QueryField(str, Enum):
    ID = "query_id"
    ID_TELEGRAM = "id_telegram"
    TYPE = "type"
    QUERY_TEXT = "query_text"


class QueryType(str, Enum):
    MAKING_TIMETABLE_BY_WORKER = "making_timetable_by_worker"
