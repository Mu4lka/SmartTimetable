import unittest

from utils.ease_sql import Database, Table


class TestTable(unittest.TestCase):
    name_database = "test_database"
    database = Database(name_database)
    name_table = "test_table"
    table = Table(name_table, database, "")

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
        sql = self.table.get_sql_to_insert({"test_field1": 1, "test_field2": "test"})
        self.assertEqual(sql, f"INSERT INTO {self.name_table} (test_field1,test_field2) VALUES (?,?)")
