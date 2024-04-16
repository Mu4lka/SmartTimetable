from abc import abstractmethod, ABC
from typing import Any

from utils.ease_sql import Database


class BaseTable(ABC):
    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    async def insert(self, *args, **kwargs):
        pass

    @abstractmethod
    async def select(self, *args, **kwargs):
        pass

    @abstractmethod
    async def found(self, *args, **kwargs):
        pass


class Table(BaseTable):
    def __init__(self, name: str, database: Database, fields: str):
        database.create_table(name, fields)
        self.__database = database
        self.__name = name

    async def delete(self, condition: str, parameters: tuple):
        self.__database.execute(
            f"DELETE FROM {self.__name} WHERE {condition}",
            parameters)

    async def insert(self, fields: dict[str, Any]):
        self.__database.execute(
            self.get_sql_to_insert(fields),
            tuple(fields.values())
        )

    async def select(
            self,
            condition: str = None,
            parameters: tuple = None,
            columns: list[str] = None):

        cursor = self.__database.execute(
            self.get_sql_to_select(condition, columns),
            parameters
        )
        return cursor.fetchall()

    async def found(self, condition: str, parameters: tuple):
        result = await self.select(condition, parameters)
        return not len(result) == 0

    def get_sql_to_insert(self, fields: dict[str, Any]):
        columns = ",".join(fields.keys())
        placeholders = ",".join(["?" for _ in range(len(fields))])
        return f"INSERT INTO {self.__name} ({columns}) VALUES ({placeholders})"

    def get_sql_to_select(self, condition: str = None, columns: list[str] = None):
        sql_columns = "*" if columns is None else ", ".join(columns)
        sql = f"SELECT {sql_columns} FROM {self.__name}"
        if condition is not None:
            sql += f" WHERE {condition}"
        return sql
