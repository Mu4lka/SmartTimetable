import secrets
import string


async def generate_key(length: int):
    letters = string.ascii_letters + string.digits
    array = []
    for _ in range(length):
        array.append(secrets.choice(letters))
    return "".join(array)
