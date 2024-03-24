from enum import Enum


class ButtonWorkerSetting(str, Enum):
    EDIT_PARAMETERS = "Редактировать параметры"
    RESET_USER = "Сбросить пользователя"
    DELETE_WORKER = "Удалить сотрудника"
