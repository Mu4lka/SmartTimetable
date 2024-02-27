from enum import Enum


class Button(str, Enum):
    CANCEL = "Отмена"


class BaseButton(str, Enum):
    SHOW_TIMETABLE = "Показать расписание"


class AdminButton(str, Enum):
    CREATE_WORKER = "Создать сотрудника"
    SHOW_WORKERS = "Показать сотрудников"
    MAKE_TIMETABLE = "Составить расписание"


class WorkerButton(str, Enum):
    SHOW_MY_TIMETABLE = "Показать мое расписание"
    MAKE_MY_TIMETABLE = "Составить мое расписание"
