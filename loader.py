from aiogram import Bot, Dispatcher

from data import config, main_path
from timetable import TimetableStorage, GoogleTimetable
from database import WorkerTable, QueryTable, ErrorTable
from utils.ease_sql import Database
from utils.google import AsyncSpreadsheets

bot = Bot(config.BOT_TOKEN)
dispatcher = Dispatcher()

spreadsheets = AsyncSpreadsheets(
    config.CREDENTIALS_FILE,
    config.SPREADSHEET_ID
)
timetable_storage = TimetableStorage(spreadsheets)
google_timetable = GoogleTimetable(spreadsheets)

database = Database(main_path + "smart_timetable.db")
worker_table = WorkerTable(database)
query_table = QueryTable(database)
error_table = ErrorTable(database)
