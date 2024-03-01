from enum import Enum


class QueryField(str, Enum):
    ID = "id"
    ID_TELEGRAM = "id_telegram"
    TYPE = "type"
    QUERY_TEXT = "query_text"


class QueryType(str, Enum):
    SENDING_TIMETABLE_BY_WORKER = "sending_timetable_by_worker"
