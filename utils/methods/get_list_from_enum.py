def get_list_from_enum(enum):
    array = []
    for item in list(enum):
        array.append(item.value)
    return array
