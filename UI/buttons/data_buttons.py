from UI.buttons.enums import ButtonWorkerSetting
from UI.buttons.enums.main_menu import BaseButton, AdminButton, WorkerButton
from utils.methods import get_list_from_enum

base_buttons = get_list_from_enum(BaseButton)
admin_buttons = base_buttons + get_list_from_enum(AdminButton)
worker_buttons = base_buttons + get_list_from_enum(WorkerButton)

worker_settings_buttons = get_list_from_enum(ButtonWorkerSetting)
