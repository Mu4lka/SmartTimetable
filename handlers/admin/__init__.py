from aiogram import Router

from handlers.admin import create_worker, coordinate_timetables, show_workers


router = Router()
router.include_routers(create_worker.router, coordinate_timetables.router, show_workers.router)
