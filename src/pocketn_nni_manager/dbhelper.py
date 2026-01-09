import sqlite3
import streamlit as st
import pandas as pd

class Varietà(object):
    def __init__(self, id: int,name: str, m: float, q: float):
        self.id = id
        self.name = name
        self.m = m
        self.q = q

@st.cache_resource
def getInstance():
    return DbHelper()

class DbHelper:

    tblName_Varieties = 'varieties'
    hasTable : bool = False

    def _get_df_from_csv(self, filename: str) -> pd.DataFrame:
        rows = pd.read_csv(filename)
        return rows

    def _get_sql_list_from_df(self, rows: pd.DataFrame) -> list[str]:
        sql_list = []
        varieties = [Varietà(rows['id'][i], rows['name'][i], rows['m'][i], rows['q'][i]) for i in range(len(rows['id']))]
        for v in varieties:
            sql_list.append(f"INSERT INTO varieties (id, name, m, q) VALUES ({v.id}, '{v.name}', {v.m}, {v.q});")
        return sql_list

    @staticmethod
    def createDb():
        if (DbHelper.hasTable):
            return
        conn = sqlite3.connect('/tmp/nni_manager.db')  # Creates a new database file if it doesn’t exist
        cursor = conn.cursor()
        listOfTables = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{DbHelper.tblName_Varieties}';").fetchall()
        if listOfTables == []:
            print('varieties Table not found!')
            cursor.execute(f"CREATE TABLE {DbHelper.tblName_Varieties}(id integer primary key autoincrement, name VARCHAR(255), m double, q double);")
            conn.commit()
            cursor.execute(f"INSERT INTO {DbHelper.tblName_Varieties}(name, m, q) VALUES (?, ?, ?);", ("Riso A", 10.02, 1.05))
            cursor.execute(f"INSERT INTO {DbHelper.tblName_Varieties}(name, m, q) VALUES (?, ?, ?);", ("Riso B", 3.70, 2.05))
            cursor.execute(f"INSERT INTO {DbHelper.tblName_Varieties}(name, m, q) VALUES (?, ?, ?);", ("Riso C", -5.58, 3.17))
            conn.commit()
            DbHelper.hasTable = True
        else:
            print('varieties Table found!')
            DbHelper.hasTable = True
        cursor.close()

    def __init__(self):
        if not DbHelper.hasTable:
            DbHelper.createDb()
            DbHelper.hasTable = True
        if (not hasattr(self, 'conn')) or (self.conn is None):
            self._setup()

    def _setup(self):
        self.conn = sqlite3.connect('/tmp/nni_manager.db', check_same_thread=False)
        # if (not hasattr(self, 'cursor')) or (self.cursor is None):
        #     self.cursor = self.conn.cursor()

    def execute(self, sql_update):
        cursor = self.conn.cursor()
        cursor.execute(sql_update)
        self.conn.commit()
        cursor.close()

    def close(self):
        self.conn.commit()
        # self.cursor.close()
        self.conn.close()

    def getVarietiesCursor(self) -> sqlite3.Cursor:
        return self.conn.execute("SELECT * FROM varieties;")

    def getVarietiesPdDataframe(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM varieties;", self.conn)
        return df

    def getVarieties(self) -> list[Varietà]:
        cur = self.getVarietiesCursor()
        rows = cur.fetchall()
        cur.close()
        varieties = [Varietà(*row) for row in rows]
        return varieties