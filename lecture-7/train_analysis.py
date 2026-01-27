# ===============================
# 1回で実行可能 完全版コード
# ===============================

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional
import os

sns.set(style="whitegrid")

# ------------------------------
# DB作成・データ挿入
# ------------------------------
DB_FILE = "stations.db"

# 既存DBがあれば削除（再実行用）
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# 駅テーブル
cur.execute("""
CREATE TABLE IF NOT EXISTS stations (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT,
    line_name TEXT,
    daily_passengers INTEGER
)
""")

# 施設テーブル
cur.execute("""
CREATE TABLE IF NOT EXISTS facilities (
    facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER,
    facility_type TEXT,
    facility_name TEXT,
    FOREIGN KEY(station_id) REFERENCES stations(station_id)
)
""")

# サンプル駅データ
stations_data = [
    ("東京", "JR山手線", 500000),
    ("新宿", "JR山手線", 750000),
    ("渋谷", "JR山手線", 600000),
    ("池袋", "JR山手線", 550000),
    ("上野", "JR山手線", 350000)
]

cur.executemany("INSERT INTO stations (station_name, line_name, daily_passengers) VALUES (?, ?, ?)", stations_data)

# サンプル施設データ
facilities_data = [
    (1, "商業", "丸ビル"),
    (1, "観光", "皇居"),
    (2, "商業", "ルミネ"),
    (2, "商業", "伊勢丹"),
    (2, "観光", "新宿御苑"),
    (3, "商業", "渋谷ヒカリエ"),
    (3, "観光", "ハチ公前"),
    (4, "商業", "東武百貨店"),
    (5, "観光", "上野動物園")
]

cur.executemany("INSERT INTO facilities (station_id, facility_type, facility_name) VALUES (?, ?, ?)", facilities_data)

conn.commit()

# ------------------------------
# 分析クラス定義
# ------------------------------
class StationAnalyzer:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)

    def get_station_facility_data(self) -> pd.DataFrame:
        query = """
        SELECT 
            s.station_id,
            s.station_name,
            s.daily_passengers,
            f.facility_type
        FROM stations s
        LEFT JOIN facilities f ON s.station_id = f.station_id
        """
        df = pd.read_sql(query, self.conn)
        # 施設数を集計
        df_count = df.groupby(['station_id', 'station_name', 'daily_passengers'])['facility_type'].count().reset_index()
        df_count.rename(columns={'facility_type': 'facility_count'}, inplace=True)
        return df_count

    def plot_facility_vs_passengers(self, df: pd.DataFrame, save_path: Optional[str]=None):
        plt.figure(figsize=(8,6))
        sns.scatterplot(data=df, x='facility_count', y='daily_passengers', hue='station_name', s=100)
        plt.title("駅別施設数と1日乗降客数の関係")
        plt.xlabel("駅周辺施設数")
        plt.ylabel("1日乗降客数")
        plt.legend(title="駅名")
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.show()

# ------------------------------
# 実行
# ------------------------------
analyzer = StationAnalyzer(DB_FILE)

# データ取得
df_analysis = analyzer.get_station_facility_data()
print("==== 駅別施設数と乗降客数 ====")
print(df_analysis)

# グラフ表示
analyzer.plot_facility_vs_passengers（df_analysis,save_path="facility_vs_passengers.png）