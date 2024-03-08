from aiogram import Router

from handlers.worker import change_shift, make_timetable, show_my_timetable

router = Router()
router.include_routers(change_shift.router, make_timetable.router, show_my_timetable.router)
