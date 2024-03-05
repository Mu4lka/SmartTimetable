from enum import Enum


class BaseButton(str, Enum):
    SHOW_TIMETABLE = "Показать расписание"


class AdminButton(str, Enum):
    CREATE_WORKER = "Создать сотрудника"
    SHOW_WORKERS = "Показать сотрудников"
    COORDINATE_TIMETABLES = "Согласование расписаний"


class WorkerButton(str, Enum):
    SHOW_MY_TIMETABLE = "Показать мое расписание"
    SEND_MY_TIMETABLE = "Отправить мое расписание"
