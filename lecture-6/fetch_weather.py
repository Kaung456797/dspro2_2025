import requests
from datetime import datetime
from database import get_connection, init_db

AREA_NAME = "東京"
AREA_CODE = "130000"
API_URL = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{AREA_CODE}.json"

def fetch_and_store():
    respone = requests.get(API_URL)
    data = response.json()
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT OR IGNORE INTO areas (area_code, area_name) VALUES (?, ?)",
        (AREA_CODE, AREA_NAME)
    )
    conn.commit()
    
    cur.execute("SELECT id FROM areas WHERE area_code = ?", (AREA_CODE,))
    area_id = cur.fetchone()[0]
    
    time_series = data[0]["timeSeries"][0]
    dates = time_series["timeDefines"]
    weathers = time_series["areas"][0]["weathers"]
    
    fetched_at = datetime.now().strftime()
    
    for d, w in zip(dates, weathers):
        cur.execute("""
            INSERT INTO forecasts (area_id, date, weather, fetched_at)
            VALUES (?, ?, ?, ?)
        """, (area_id, d[:10], w, fetched_at))
        
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    init_db()
    fetch_and_store()
    print("天気データを取得してデータベースに保存しました。")
            
            

        