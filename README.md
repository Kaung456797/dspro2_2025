# 気象庁APIを利用した天気予報アプリ（個人課題3）

## 概要
本アプリは、前回課題で作成した天気予報アプリを改良し、
気象庁APIから取得した天気情報をSQLiteデータベースに保存し、
DBから取得したデータを表示するアプリである。

## 使用技術
- Python
- Flet
- SQLite
- 気象庁API

## 工夫点
- JSONデータを直接表示せず、DBに保存してから表示する構成とした
- エリア情報と天気予報を分離し、正規化を行った
- UIにはCardやアイコンを用い、視覚的に分かりやすくした

## 実行方法
```bash
pip install -r requirements.txt
python fetch_weather.py
python app.py
