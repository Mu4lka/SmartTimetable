from enum import Enum


class Button(str, Enum):
    CANCEL = "Отмена"


class BaseButton(str, Enum):
    SHOW_TIMETABLE = "Показать расписание"


class AdminButton(str, Enum):
    CREATE_WORKER = "Создать сотрудника"
    SHOW_WORKERS = "Показать сотрудников"
    GENERATE_TIMETABLE = "Сгенерировать расписание"


class WorkerButton(str, Enum):
    SHOW_MY_TIMETABLE = "Показать мое расписание"
    CHANGE_SHIFT = "Изменить смену"
    SELECT_WEEKEND = "Выбрать выходные"
