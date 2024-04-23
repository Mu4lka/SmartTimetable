import json
import os
import sys
import keyboard


def get_json_from_file(path: str, json_data: dict):
    if not os.path.exists(path):
        create_json_file(path, json_data)
        print(f"[WARNING] Could not find file named {path}! "
              f"Restart the application!")
        keyboard.read_key()
        sys.exit()

    with open(path) as file:
        return json.load(file)


def create_json_file(path: str, json_data: dict):
    with open(path, 'w') as file:
        json.dump(json_data, file)
