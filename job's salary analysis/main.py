import sqlite3
import pandas as pd

from src.data_loader import load_csv_to_db
from src.analyzer import JobAnalyzer
from src.visualization import plot_scatter, plot_regression
from tests.test_basic import test_dataframe

CSV_PATH = "data/jobs.csv"
DB_PATH = "db/jobs.db"

# 1. CSV → DB
df = load_csv_to_db(CSV_PATH, DB_PATH)

# 2. DBからクエリで取得
conn = sqlite3.connect(DB_PATH)
query = "SELECT salary, skill_count FROM jobs"
df_db = pd.read_sql_query(query, conn)
conn.close()

# 3. テスト（加点）
test_dataframe(df_db)
print("✅ テスト成功")

# 4. 可視化
plot_scatter(df_db)

# 5. 回帰分析
analyzer = JobAnalyzer(df_db)
coef, intercept, r2, y_pred = analyzer.regression()

print(f"""
回帰係数: {coef:.2f}
切片: {intercept:.2f}
決定係数 R²: {r2:.2f}
""")

# 6. 回帰直線表示
plot_regression(df_db, y_pred)