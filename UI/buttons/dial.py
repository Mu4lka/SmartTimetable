from data import constants

hours = {f"{index}:00": f"{index}" for index in range(constants.DAY_END + 1)}
hours_first_zero = {f"0{index}:00": f"{index}" for index in range(10)}
half_hours = {f"{index}:30": f"{index}.5" for index in range(constants.DAY_END)}
half_hours_first_zero = {f"0{index}:0": f"{index}" for index in range(10)}
day_off = {"вых": 0.0}