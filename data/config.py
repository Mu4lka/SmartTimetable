from data import constants
from utils.methods import get_json_from_file

config_file_name = "config.json"
config = get_json_from_file(config_file_name, constants.config_example)

BOT_TOKEN = config["bot_token"]
ADMIN_IDS = config["admin_ids"]

LINK_TO_TIMETABLE = config["link_to_timetable"]
CREDENTIALS_FILE = config["credentials_file"]
SPREADSHEET_ID = config["spreadsheet_id"]
