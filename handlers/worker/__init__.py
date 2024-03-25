from aiogram import Router

from handlers.worker import send_timetable, show_my_timetable

router = Router()
router.include_routers(send_timetable.router, show_my_timetable.router)
