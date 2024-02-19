from enum import Enum


class WorkerSetting(str, Enum):
    EDIT_PARAMETERS = "Редактировать параметры"
    RESTORE_ACCESS = "Восстановить доступ"
    DELETE_WORKER = "Удалить сотрудника"
