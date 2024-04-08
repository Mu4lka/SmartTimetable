from aiogram import Bot

from data.config import ADMIN_IDS
from data.constants import START_BOT


async def on_startup_notify(bot: Bot):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, START_BOT)
        except Exception as error:
            print(f"Error: {error}. Unfortunately, I could not send a message to the admin. Admin ID: {admin_id}")
