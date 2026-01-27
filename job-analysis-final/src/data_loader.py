import pandas as pd
import sqlite3
import os

def load_csv_to_db(csv_path, db_path):
    # CSV読み込み
    df = pd.read_csv(csv_path)

    # 前処理
    df = df.dropna(subset=["salary", "skill_count"])
    df["salary"] = df["salary"].astype(int)
    df["skill_count"] = df["skill_count"].astype(int)

    # DBフォルダがなければ作成
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # SQLiteへ保存
    conn = sqlite3.connect(db_path)
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.close()

    return df