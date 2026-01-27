import sqlite3
import pandas as pd

conn = sqlite3.connect("jobs.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area TEXT,
    title TEXT,
    salary INTEGER,
    skills TEXT
)
""")

df = pd.read_csv("jobs.csv")

def salary_to_int(s):
    s = s.replace("万円", "").replace("月給", "")
    try:
        return int(s)
    except:
        return None

df["salary"] = df["salary"].apply(salary_to_int)

df.to_sql("jobs", conn, if_exists="append", index=False)
conn.commit()
conn.close()

print("DB保存完了")