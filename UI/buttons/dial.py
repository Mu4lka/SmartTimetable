from data import constants


def make_dial(count: int, accuracy: str = "00", zeroing: int = ""):
    value = 0
    if accuracy == "30":
        value = 5
    return {f"{zeroing}{index}:{accuracy}": f"{index}.{value}" for index in range(count)}


hours = make_dial(constants.DAY_END + 1)
hours_first_zero = make_dial(10, zeroing=0)
half_hours = make_dial(constants.DAY_END, "30")
half_hours_first_zero = make_dial(10, "30", 0)