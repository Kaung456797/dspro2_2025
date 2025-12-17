import flet as ft
import requests

AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"

def get_forecast(area_code):
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    return requests.get(url).json()

def weather_card(date, weather, min_t, max_t):
    icon = ft.icons.WB_SUNNY
    if "雨" in weather:
        icon = ft.icons.UMBRELLA
    elif "曇" in weather:
        icon = ft.icons.CLOUD

    return ft.Card(
        content=ft.Container(
            width=150,
            padding=15,
            border_radius=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(date, weight="bold"),
                    ft.Icon(icon, size=40, color=ft.colors.ORANGE),
                    ft.Text(weather),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(f"{min_t}℃", color=ft.colors.BLUE),
                            ft.Text(" / "),
                            ft.Text(f"{max_t}℃", color=ft.colors.RED),
                        ],
                    ),
                ],
            ),
        )
    )

def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.bgcolor = "#B0BEC5"

    # ---------- 天気表示エリア ----------
    forecast_view = ft.Row(
    wrap=True,
    spacing=20,
    scroll=ft.ScrollMode.AUTO
)

    def load_weather(area_code):
        forecast_view.controls.clear()
        data = get_forecast(area_code)

        times = data[0]["timeSeries"][0]
        temps = data[0]["timeSeries"][2]

        for i in range(len(times["timeDefines"])):
            date = times["timeDefines"][i][:10]
            weather = times["areas"][0]["weathers"][i]
            min_t = temps["areas"][0]["tempsMin"][i] or "-"
            max_t = temps["areas"][0]["tempsMax"][i] or "-"
            forecast_view.controls.append(
                weather_card(date, weather, min_t, max_t)
            )
        page.update()

    # ---------- サイドバー ----------
    sidebar = ft.Container(
        width=260,
        bgcolor="#607D8B",
        padding=10,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("地域を選択", size=16, color="white"),
                ft.Divider(color="white"),
                ft.ExpansionTile(
                    title=ft.Text("関東地方", color="white"),
                    controls=[
                        ft.ListTile(
                            title=ft.Text("東京都", color="white"),
                            on_click=lambda e: load_weather("130000"),
                        ),
                        ft.ListTile(
                            title=ft.Text("千葉県", color="white"),
                            on_click=lambda e: load_weather("120000"),
                        ),
                        ft.ListTile(
                            title=ft.Text("埼玉県", color="white"),
                            on_click=lambda e: load_weather("110000"),
                        ),
                    ],
                ),
                ft.ExpansionTile(
                    title=ft.Text("北海道地方", color="white"),
                    controls=[
                        ft.ListTile(
                            title=ft.Text("北海道", color="white"),
                            on_click=lambda e: load_weather("010000"),
                        ),
                    ],
                ),
            ],
        ),
    )

    # ---------- レイアウト ----------
    page.add(
        ft.Column(
            controls=[
                ft.AppBar(
                    title=ft.Text("天気予報", size=20),
                    bgcolor=ft.colors.DEEP_PURPLE,
                ),
                ft.Row(
                    expand=True,
                    controls=[
                        sidebar,
                        ft.Container(
                            expand=True,
                            padding=20,
                            content=forecast_view,
                        ),
                    ],
                ),
            ],
        )
    )

    load_weather("130000")  # 初期表示（東京）

ft.app(target=main)