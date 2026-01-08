import sqlite3
import pandas as pd

class Varietà(object):
    def __init__(self, id: int,name: str, m: float, q: float):
        self.id = id
        self.name = name
        self.m = m
        self.q = q

class DbHelper:

    hasTable : bool = False

    @staticmethod
    def createDb():
        if (DbHelper.hasTable):
            return
        conn = sqlite3.connect('/tmp/nni_manager.db')  # Creates a new database file if it doesn’t exist
        cursor = conn.cursor()
        tblName = 'varieties'
        listOfTables = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tblName}';").fetchall()
        if listOfTables == []:
            print('varieties Table not found!')
            cursor.execute(f"CREATE TABLE {tblName}(id integer primary key autoincrement, name VARCHAR(255), m double, q double);")
            conn.commit()
            cursor.execute(f"INSERT INTO {tblName}(name, m, q) VALUES (?, ?, ?);", ("Riso A", 10.02, 1.05))
            cursor.execute(f"INSERT INTO {tblName}(name, m, q) VALUES (?, ?, ?);", ("Riso B", 3.70, 2.05))
            cursor.execute(f"INSERT INTO {tblName}(name, m, q) VALUES (?, ?, ?);", ("Riso C", -5.58, 3.17))
            conn.commit()
            DbHelper.hasTable = True
        else:
            print('varieties Table found!')
            DbHelper.hasTable = True
        conn.close()

    def __init__(self):
        if not DbHelper.hasTable:
            DbHelper.createDb()
            DbHelper.hasTable = True
        if (not hasattr(self, 'cursor')) or (self.cursor is None):
            self.setup()

    def setup(self) -> sqlite3.Cursor:
        if (not hasattr(self, 'conn')) or (self.conn is None):
            self.conn = sqlite3.connect('/tmp/nni_manager.db')
        if (not hasattr(self, 'cursor')) or (self.cursor is None):
            self.cursor = self.conn.cursor()
        return self.cursor

    def close(self):
        self.cursor.close()
        self.conn.close()

    def getVarietiesCursor(self) -> sqlite3.Cursor:
        return self.cursor.execute("SELECT id, name, m, q FROM varieties;")

    def getVarietiesDataframe(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT id, name, m, q FROM varieties;", self.conn)
        return df

    def getVarieties(self) -> list[Varietà]:
        cur = self.getVarietiesCursor()
        rows = cur.fetchall()
        varieties = [Varietà(*row) for row in rows]
        return varieties