import pandas as pd
import sqlite3

def load_csv_to_db(csv_path, db_path):
    df = pd.read_csv(csv_path)

    df = df.dropna(subset=["salary", "skill_count"])
    df["salary"] = df["salary"].astype(int)
    df["skill_count"] = df["skill_count"].astype(int)

    conn = sqlite3.connect(db_path)
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.close()

    return df