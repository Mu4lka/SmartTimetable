async def get_message_parameters(descriptions: dict[str: str], values: dict):
    message = ""
    for item in descriptions:
        message = message + f"{descriptions[item]}: {values.get(item)}\n"
    return message
