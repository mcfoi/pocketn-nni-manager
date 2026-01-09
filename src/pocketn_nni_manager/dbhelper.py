import logging
import os
import sqlite3
import streamlit as st
import pandas as pd

class Varietà(object):
    def __init__(self, id: int,name: str, m: float, q: float, nni_cap: float = 1.60):
        self.id = id
        self.name = name
        self.m = m
        self.q = q
        self.nni_cap = nni_cap  # Default NNI cap value

@st.cache_resource
def getInstance():
    return DbHelper()

class DbHelper:

    tblName_Varieties = 'varieties'
    hasTable : bool = False

    @staticmethod
    def _get_df_from_csv(filename: str) -> pd.DataFrame:
        rows = pd.read_csv(filename)
        return rows

    @staticmethod
    def _get_sql_list_from_df(rows: pd.DataFrame) -> list[str]:
        sql_list = []
        varieties = [Varietà(rows['id'][i], rows['name'][i], rows['m'][i], rows['q'][i], rows['nni_cap'][i]) for i in range(len(rows['id']))]
        for v in varieties:
            sql_list.append(f"INSERT INTO varieties (id, name, m, q, nni_cap) VALUES ({v.id}, '{v.name}', {v.m}, {v.q}, {v.nni_cap});")
        return sql_list

    @staticmethod
    def createDb():
        if (DbHelper.hasTable):
            return
        dataDir = os.getenv("STREAMLIT_DATA_DIR", "/tmp")
        conn = sqlite3.connect(f'{dataDir}/nni_manager.db')  # Creates a new database file if it doesn’t exist
        cursor = conn.cursor()
        listOfTables = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{DbHelper.tblName_Varieties}';").fetchall()
        if listOfTables == []:
            print('varieties Table not found!')
            cursor.execute(f"CREATE TABLE {DbHelper.tblName_Varieties}(id integer primary key autoincrement, name VARCHAR(255), m double, q double, nni_cap double);")
            conn.commit()
            df = DbHelper._get_df_from_csv(f'{dataDir}/varieties.csv')
            if (df is not None) and (len(df) > 0):
                sql_list = DbHelper._get_sql_list_from_df(df)
                for sql in sql_list:
                    cursor.execute(sql)
            else:
                cursor.execute(f"INSERT INTO {DbHelper.tblName_Varieties}(name, m, q, nni_cap) VALUES (?, ?, ?, ?);", ("Riso Aaa", 10.02, 1.05, 1.60))
                cursor.execute(f"INSERT INTO {DbHelper.tblName_Varieties}(name, m, q, nni_cap) VALUES (?, ?, ?, ?);", ("Riso Bbb", 3.70, 2.05, 1.60))
                cursor.execute(f"INSERT INTO {DbHelper.tblName_Varieties}(name, m, q, nni_cap) VALUES (?, ?, ?, ?);", ("Riso Ccc", -5.58, 3.17, 1.60))
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
        dataDir = os.getenv("STREAMLIT_DATA_DIR", "/tmp")
        self.conn = sqlite3.connect(f'{dataDir}/nni_manager.db', check_same_thread=False)

    def execute(self, sql_update):
        _logger = logging.getLogger("NNIManager")
        cursor = self.conn.cursor()
        cursor.execute(sql_update)
        self.conn.commit()
        return cursor

    def close(self):
        self.conn.commit()
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