import sqlite3


class Database:
    def __init__(self, path: str):
        self.__path = path

    def execute(self, sql: str, parameters: tuple = None):
        with sqlite3.connect(f"{self.__path}") as connection:
            cursor = connection.cursor()
            if parameters is None:
                parameters = ()
            cursor.execute(sql, parameters)
            connection.commit()
        return cursor

    def create_table(self, name, fields: str):
        self.execute(
            f"""CREATE TABLE IF NOT EXISTS {name}({fields})"""
        )
