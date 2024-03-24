from enum import Enum


class OtherButton(str, Enum):
    MAIN_MENU = "Главное меню"
    CHANGE_SHIFT = "Поменять смену"
    SKIP = "Пропустить"
    BEGIN = "Начать"
    CHANGE = "Изменить"
    SEND_TIMETABLE = "Отправить расписание"
    ACCEPT = "Принять"
    REJECT = "Отклонить"
