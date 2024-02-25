from enum import Enum


class OtherButton(str, Enum):
    CHANGE_SHIFT = "Поменять смену"
    QUICKLY_CREATE = "Быстро создать"
    CREATE_MANUALLY = "В ручную создать"
