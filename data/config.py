from utils.methods import get_json_from_file

config_file_name = "config.json"

config_example = {
    "bot_token": "токен бота",
    "admin_ids": [1000000000, 1111111111],
    "link_to_timetable": "Cсылка на гугл таблицу",
    "credentials_file": "название файла реквизитов для входа сервисного аккаунта",
    "spreadsheet_id": "Aйди гугл таблицы"
}

config = get_json_from_file(config_file_name, config_example)

BOT_TOKEN = config["bot_token"]
ADMIN_IDS = config["admin_ids"]

LINK_TO_TIMETABLE = config["link_to_timetable"]
CREDENTIALS_FILE = config["credentials_file"]
SPREADSHEET_ID = config["spreadsheet_id"]
