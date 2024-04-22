from data.config import ADMIN_IDS
from loader import bot


async def send_message_all_admins(message: str):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, message)
        except Exception as error:
            print(f"[WARNING] Failed to send message to admin!"
                  f"Id: {admin_id}\nDetails: {error}")
