import flet as ft
from database import get_connection

def weather_card(date,weather):
    icon = ft.icons.WB_SUNNY
    if "雨" in weather:
        icon = ft.icons.UMBRELLA
    elif "雲" in weather:
        icon = ft.icons.WB_CLOUDY
        
    return ft.Card(
        content=ft.Container(
            width=160,
            padding=10,
            bgcolor="white",
            border_radius=10,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(date,weight=ft.FontWeight.BOLD),
                    ft.Icon(icon,size=36,color=ft.colors.ORANGE),
                    ft.Text(weather),
                ],
            ),
        ),
    )
    
def main(page: ft.Page):
    page.title = "天気予報(データベース版)"
    page.bgcolor = "#ECEFF1"
    
    forecast_area = ft.Row(wrap=True,spacing=12)
    
    def load_weather_data(e):
        forecast_area.controls.clear()
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT date, weather 
            FROM forecasts
            ORDER BY date
            LIMIT 7
        """)
    for d, w in cur.fetchall():
        forecast_area.controls.append(weather_card(d, w))
    conn.close()
    page.update()
    
    page.add(
        ft.Column(
            controls=[
                ft.ElevatedButton("天気データ読み込み", on_click=load_weather_data),
                forecast_area,
            ]
        )
    )
    
ft.app(target=main)          
