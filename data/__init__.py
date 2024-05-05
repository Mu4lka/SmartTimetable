from .json_files import Save, Settings, Config

first_path = "../data/"

save = Save(first_path + "save.json")
config = Config(first_path + "config.json")
settings = Settings(first_path + "settings.json")
