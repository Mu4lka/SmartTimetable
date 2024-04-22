import json
import os
import sys
import keyboard


def get_json_from_file(path: str, json_data: dict):
    if not os.path.exists(path):
        create_json_file(path, json_data)
        print(f"File {path} was not found, after which it was created,"
              f"Change the data and restart the application")
        keyboard.read_key()
        sys.exit()

    with open(path) as file:
        return json.load(file)


def create_json_file(path: str, json_data: dict):
    with open(path, 'w') as file:
        json.dump(json_data, file)
