from .json_files import Save, Settings, Config

main_path = "../data/"

save = Save(main_path + "save.json")
config = Config(main_path + "config.json")
settings = Settings(main_path + "settings.json")
