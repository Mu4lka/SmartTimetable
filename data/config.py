from utils.get_config import get_config

config_file_name = "config.json"
config = get_config(config_file_name)

BOT_TOKEN = config["bot_token"]
ADMIN_IDS = config["admin_ids"]

LINK_TO_TIMETABLE = config["link_to_timetable"]
CREDENTIALS_FILE = config["credentials_file"]
SPREADSHEET_ID = config["spreadsheet_id"]
