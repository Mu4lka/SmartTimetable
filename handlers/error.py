from aiogram import Router

from aiogram.types import ErrorEvent


router = Router()


# @router.error()
# async def error_handler(event: ErrorEvent):
#     with open("errors.txt", "w") as file:
#         file.write(str(event))
