import mysql.connector as mariadb
from typing import List, Any
from antlr.FileSyntaxErrorListener import *


class Column:
    cn: str
    dt: str

    def __init__(self, column_name: str, data_type: str):
        self.cn = column_name
        self.dt = data_type

    def format_create_table(self) -> str:
        return "`" + self.cn + "` " + self.dt


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


class Row:
    __values: list

    def __init__(self):
        self.__values = []

    def append(self, string: str) -> None:
        self.__values.append(string)

    def format(self) -> str:
        result: str = "("
        for value in self.__values:
            result += "'" + str(value) + "',"
        result = result[:-1]
        result += ")"
        return result

    def __add__(self, other):
        result = Row()
        result.__values = self.__values + other.__values
        return result


class DBController:
    USER: [str] = "upsim"
    PASSWORD: [str] = "upsim"
    DATABASE: [str] = "upsimdb"

    mariadb_connection: Any

    def __init__(self):
        self.mariadb_connection = mariadb.connect(
            user=self.USER,
            password=self.PASSWORD,
            database=self.DATABASE
        )

    def __del__(self):
        self.mariadb_connection.close()

    def cursor(self):
        return self.mariadb_connection.cursor()

    def drop_table(self, table_name: str) -> None:
        self.cursor().execute("DROP TABLE IF EXISTS `%s`;" % table_name)

    def get_result(self, command: str) -> Any:
        c = self.cursor()
        c.execute(command)
        return c.fetchall()

    def show_tables(self):
        return self.get_result("SHOW TABLES;")

    def create_table(
            self,
            table_name: str,
            table_description: TableDescription
    ) -> None:
        self.drop_table(table_name)
        self.cursor().execute(
            "CREATE TABLE `%s` (%s);" %
            (table_name, table_description.format_create_table())
        )

    def describe_table(self, table_name: str):
        return self.get_result("DESCRIBE `%s`;" % table_name)

    def select_all_from_table(self, table_name: str):
        return self.get_result(
            "SELECT %s FROM `%s`;" %
            ("*", table_name)
        )

    def select_some_from_table(self, table_name: str, column_list: List[str]):
        columns: str = ""
        for column in column_list:
            columns += "`" + column + "`,"
        columns = columns[:-1]
        return self.get_result(
            "SELECT %s "
            "FROM %s A INNER JOIN "
            "(SELECT ICN, MAX(SSN) maximum FROM %s "
            "GROUP BY ICN) B ON B.ICN = A.ICN AND B.maximum = A.SSN;" %
            (columns, table_name, table_name)
        )

    @staticmethod
    def format_row_list(rows: List[Row]) -> str:
        result: str = ""
        for row in rows:
            result += row.format() + ','
        result = result[:-1]
        return result

    INSERT_SYNTAX: [str] = "INSERT `%s` VALUES %s;"

    def insert_rows(self, table_name: str, rows: List[Row]) -> None:
        self.cursor().execute(
            self.INSERT_SYNTAX %
            (table_name, self.format_row_list(rows))
        )

    def insert_row(self, table_name: str, row: Row, commit: bool = False) -> None:
        self.cursor().execute(
            self.INSERT_SYNTAX %
            (table_name, row.format())
        )
        if commit:
            self.commit()

    def commit(self) -> None:
        self.mariadb_connection.commit()
