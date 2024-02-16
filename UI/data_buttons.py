from enums.menu import BaseButton, AdminButton, WorkerButton
from utils.get_array_from_enum import get_array_from_enum


base_buttons = get_array_from_enum(BaseButton)
admin_buttons = base_buttons + get_array_from_enum(AdminButton)
worker_buttons = base_buttons + get_array_from_enum(WorkerButton)
