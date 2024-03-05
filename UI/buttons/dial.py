from data import constants


def make_dial(hours: int, is_half_hours: bool = False, zeroing: bool = False):
    zero = ""
    if zeroing:
        zero = "0"
    return {f"{zero}{hour}:{3 * is_half_hours}0": f"{hour + 0.5 * is_half_hours}" for hour in range(hours)}


hours = make_dial(constants.DAY_END + 1)
zeroing_hours = make_dial(10, zeroing=True)
half_hours = make_dial(constants.DAY_END, True)
zeroing_half_hours = make_dial(10, True, True)
full_dial = {**hours, **half_hours, **zeroing_hours, **zeroing_half_hours}
