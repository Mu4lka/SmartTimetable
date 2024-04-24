import sys

import keyboard

from data import constants
from loader import bot


async def check_license():
    try:
        await bot.send_message(constants.CREATOR_ID, "Подписан")
    except Exception:
        print("[ERROR] Failed to pass licensing!")
        keyboard.read_key()
        sys.exit()
