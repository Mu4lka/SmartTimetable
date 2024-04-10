from aiogram import Bot, Dispatcher

from data import config
from timetable import Timetable

bot = Bot(config.BOT_TOKEN)

timetable = Timetable()
dispatcher = Dispatcher()
