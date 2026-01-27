import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = "https://example.com/jobs"  # ← 実際のURLに変更
AREAS = ["東京", "大阪", "福岡"]

data = []

for area in AREAS:
    print(f"{area}のデータ取得中...")
    params = {"area": area}

    r = requests.get(BASE_URL, params=params)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = soup.select(".job-card")

    for job in jobs:
        title = job.select_one(".title").text
        salary = job.select_one(".salary").text
        skills = job.select_one(".skills").text

        data.append({
            "area": area,
            "title": title,
            "salary": salary,
            "skills": skills
        })

    time.sleep(1)  # サーバ負荷対策（重要）

df = pd.DataFrame(data)
df.to_csv("jobs.csv", index=False)
print("CSV保存完了")