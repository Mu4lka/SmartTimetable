from enums.menu import BaseButton, AdminButton, WorkerButton
from enums.worker_setting import WorkerSetting
from utils.get_array_from_enum import get_array_from_enum


base_buttons = get_array_from_enum(BaseButton)
admin_buttons = base_buttons + get_array_from_enum(AdminButton)
worker_buttons = base_buttons + get_array_from_enum(WorkerButton)

worker_settings_buttons = get_array_from_enum(WorkerSetting)
