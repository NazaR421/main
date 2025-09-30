import sqlite3
from settings import *

db_name = "blog.db"
conn = None
cursor = None


def get_cursor():
    conn = sqlite3.connect(PATH + db_name)
    conn.row_factory = sqlite3.Row
    return conn.cursor()

def close_connection(conn):
    conn.close()




