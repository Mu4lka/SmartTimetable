import unittest

from utils.ease_sql import Database, Table


class TestTable(unittest.TestCase):
    name_database = "test_database"
    database = Database(name_database)
    name_table = "test_table"
    table = Table(name_table, database, "column1 TEXT, column2 TEXT")

    def test_get_sql_to_select(self):
        sql = self.table.get_sql_to_select(
            "condition",
            ["column1", "column2"]
        )
        self.assertEqual(sql, f"SELECT column1, column2 FROM {self.name_table} WHERE condition")

        sql = self.table.get_sql_to_select(columns=["column1", "column2"])
        self.assertEqual(sql, f"SELECT column1, column2 FROM {self.name_table}")

        sql = self.table.get_sql_to_select(condition="condition")
        self.assertEqual(sql, f"SELECT * FROM {self.name_table} WHERE condition")

        sql = self.table.get_sql_to_select()
        self.assertEqual(sql, f"SELECT * FROM {self.name_table}")

    def test_get_sql_to_insert(self):
        sql = self.table.get_sql_to_insert({"column1": 1, "column2": "test"})
        self.assertEqual(sql, f"INSERT INTO {self.name_table} (column1,column2) VALUES (?,?)")

    def test_get_sql_to_update(self):
        sql = self.table.get_sql_to_update(["column1", "column2"], "condition")
        self.assertEqual(sql, "UPDATE test_table SET column1 = ?, column2 = ? WHERE condition")
