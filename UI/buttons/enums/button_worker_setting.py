from enum import Enum


class ButtonWorkerSetting(str, Enum):
    CHANGE_PARAMETER = "Изменить параметр"
    RESET_USER = "Сброс пользователя"
    DELETE_WORKER = "Удалить сотрудника"
