from aiogram import Bot, Dispatcher

from data import config
from data.config import SPREADSHEET_ID, CREDENTIALS_FILE
from timetable import TimetableStorage, GoogleTimetable
from database import WorkerTable, QueryTable
from utils.ease_sql import Database
from utils.google import AsyncSpreadsheets

bot = Bot(config.BOT_TOKEN)
dispatcher = Dispatcher()

spreadsheets = AsyncSpreadsheets(CREDENTIALS_FILE, SPREADSHEET_ID)
timetable_storage = TimetableStorage(spreadsheets)
google_timetable = GoogleTimetable(spreadsheets)

database = Database("smart_timetable")
worker_table = WorkerTable(database)
query_table = QueryTable(database)
