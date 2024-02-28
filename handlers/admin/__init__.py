from aiogram import Router

from handlers.admin import create_worker, make_timetable, show_workers


router = Router()
router.include_routers(create_worker.router, make_timetable.router, show_workers.router)
