async def make_form(data: dict, delimiter: str = ": "):
    items = []
    for key, value in list(data.items()):
        items.append(f"{key}{delimiter}{value}\n")
    return "".join(items)
