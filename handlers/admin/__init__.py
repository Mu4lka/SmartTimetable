from aiogram import Router

from handlers.admin import add_worker, coordinate_timetables, show_workers


router = Router()
router.include_routers(add_worker.router, coordinate_timetables.router, show_workers.router)
