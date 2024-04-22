from data import constants
from utils.methods import send_message_all_admins


async def on_startup_notify():
    await send_message_all_admins(constants.START_BOT)
