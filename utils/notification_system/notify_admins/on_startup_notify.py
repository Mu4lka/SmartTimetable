from aiogram import Bot

from data import constants
from data.config import ADMIN_IDS


async def on_startup_notify(bot: Bot):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, constants.START_BOT)
        except Exception as error:
            print(f"[WARNING] Failed to send message to admin!"
                  f"Id: {admin_id}\nDetails: {error}")
