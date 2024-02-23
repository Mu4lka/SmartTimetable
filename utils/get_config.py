import json
import os
import sys
import keyboard


def get_config(path: str):
    if not os.path.exists(path):
        create_config(path)
        keyboard.read_key()
        sys.exit()

    with open(path) as path:
        return json.load(path)


def create_config(path: str):
    with open(path, 'w') as config_path:
        config = {
            "bot_token": "токен бота",
            "admin_ids": [1000000000, 1111111111],
            "link_to_timetable": "Cсылка на гугл таблицу",
            "credentials_file": "название файла реквизитов для входа сервисного аккаунта",
            "spreadsheet_id": "Aйди гугл таблицы"
        }
        json.dump(config, config_path)
        print(f"Не нашел файл {path}, в следствии чего он был создан, "
              f"поменяйте в нем данные и перезапустите приложение")
