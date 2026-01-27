import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

class JobAnalyzer:
    def __init__(self, area):
        self.area = area
        self.conn = sqlite3.connect("jobs.db")

    def avg_salary(self):
        query = """
        SELECT AVG(salary) as avg_salary
        FROM jobs
        WHERE area = ?
        """
        df = pd.read_sql(query, self.conn, params=(self.area,))
        return df["avg_salary"][0]

    def skill_count(self, skill):
        query = """
        SELECT COUNT(*) as count
        FROM jobs
        WHERE skills LIKE ?
        """
        df = pd.read_sql(query, self.conn, params=(f"%{skill}%",))
        return df["count"]

areas = ["東京", "大阪", "福岡"]
avg_salaries = []

for area in areas:
    analyzer = JobAnalyzer(area)
    avg_salaries.append(analyzer.avg_salary())

plt.bar(areas, avg_salaries)
plt.title("地域別平均給与")
plt.ylabel("平均給与（万円）")
plt.show()