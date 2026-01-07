-- areas テーブル
CREATE TABLE areas (
    area_id INTEGER PRIMARY KEY,
    area_name TEXT NOT NULL,
    area_code TEXT UNIQUE NOT NULL
);

-- forecasts テーブル
CREATE TABLE forecasts (
    forecast_id INTEGER PRIMARY KEY,
    area_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    weather TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    FOREIGN KEY (area_id) REFERENCES areas(area_id)
);