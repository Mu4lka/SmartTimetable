import secrets
import string

from data import constants


async def generate_key(length=constants.KEY_LENGTH):
    letters = string.ascii_letters + string.digits
    array = []
    for _ in range(length):
        array.append(secrets.choice(letters))
    return "".join(array)
