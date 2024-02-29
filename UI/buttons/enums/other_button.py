from enum import Enum


class OtherButton(str, Enum):
    CANCEL = "Отмена"
    CHANGE_SHIFT = "Поменять смену"
    SKIP = "Пропустить"
    BEGIN = "Начать"
