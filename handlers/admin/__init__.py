from aiogram import Router

from handlers.admin import add_worker, coordinate_timetable_elements, show_workers


router = Router()
router.include_routers(
    add_worker.router,
    coordinate_timetable_elements.router,
    show_workers.router
)
