from data import constants, settings
from utils.methods import send_message_all_admins


async def on_startup_notify():
    if not settings.IS_NOTIFY_START_UP:
        return
    await send_message_all_admins(constants.START_BOT)
