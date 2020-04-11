import mysql.connector as mariadb
from typing import Final, List
from FileSyntaxErrorListener import *


class Column:
    cn: str
    dt: str

    def __init__(self, column_name: str, data_type: str):
        self.cn = column_name
        self.dt = data_type

    def format_create_table(self) -> str:
        return self.cn + " " + self.dt


class TableDescription:
    columns: List[Column]

    def __init__(self, columns: List[Column]):
        if len(columns) == 0:
            raise Exception(ERROR_EMPTY_TABLE_DESCRIPTION)
        self.columns = columns

    def format_create_table(self) -> str:
        result: str = ""
        for column in self.columns:
            result += column.format_create_table() + ","
        result = result[:-1]
        return result


class DBController:
    USER: Final[str] = "upsim"
    PASSWORD: Final[str] = "upsim"
    DATABASE: Final[str] = "upsimdb"

    def __init__(self):
        mariadb_connection = mariadb.connect(
            user=self.USER,
            password=self.PASSWORD,
            database=self.DATABASE
        )
        self.cursor = mariadb_connection.cursor()

    def drop_table(self, table_name: str) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")

    def create_table(
            self,
            table_name: str,
            table_description: TableDescription
    ) -> None:
        self.drop_table(table_name)
        self.cursor.execute(
            "CREATE TABLE " +
            table_name +
            " (" +
            table_description.format_create_table()+
            ");"
        )

