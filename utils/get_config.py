import json
import os
import sys
import keyboard


def get_config(path: str, config_example: dict):
    if not os.path.exists(path):
        create_config_file(path, config_example)
        print(f"File {path} was not found, after which it was created,"
              f"Change the data and restart the application")
        keyboard.read_key()
        sys.exit()

    with open(path) as path:
        return json.load(path)


def create_config_file(path: str, config_example: dict):
    with open(path, 'w') as config_path:
        json.dump(config_example, config_path)
