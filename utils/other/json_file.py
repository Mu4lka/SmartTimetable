import json
import logging


class JsonFile:
    def __init__(self, path: str):
        self._path = path
        self.setup()

    def unload(self):
        data_to_dump = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                data_to_dump.update({key: value})
        with open(self._path, 'w') as file:
            json.dump(data_to_dump, file)

    def download(self):
        with open(self._path, 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    logging.warning(f"Ignoring unknown attribute '{key}'")

    def setup(self):
        try:
            self.download()
        except FileNotFoundError:
            logging.error(f"File '{self._path}' not found.")
            self.unload()
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON file '{self._path}': {e}")
            self.unload()
