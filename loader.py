from aiogram import Bot, Dispatcher

from data import config
from data.config import SPREADSHEET_ID, CREDENTIALS_FILE
from timetable import Timetable
from database import WorkerTable, QueryTable
from utils.ease_sql import Database

bot = Bot(config.BOT_TOKEN)
dispatcher = Dispatcher()

timetable = Timetable(CREDENTIALS_FILE, SPREADSHEET_ID)

database = Database("smart_timetable")
worker_table = WorkerTable(database)
query_table = QueryTable(database)
