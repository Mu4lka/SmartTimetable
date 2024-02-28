from enum import Enum


class ButtonWorkerSetting(str, Enum):
    EDIT_PARAMETERS = "Редактировать параметры"
    RESTORE_ACCESS = "Восстановить доступ"
    DELETE_WORKER = "Удалить сотрудника"
