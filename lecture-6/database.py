import sqlite3

DB_NAME = 'weather.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with open('schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
        
    conn = get_connection()
    conn.executescript(sql)
    conn.close()