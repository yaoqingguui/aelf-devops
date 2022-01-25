import os
import sqlite3 as sqlite
from config import LoadConf


class MyDB(LoadConf):
    def __init__(self):
        self.db_file = os.path.join(os.path.dirname(__file__), 'sqlite3/my.db')

    def execute_select(self, sql):
        conn = sqlite.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        data_info = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return data_info

    def execute_up(self, sql):
        conn = sqlite.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
