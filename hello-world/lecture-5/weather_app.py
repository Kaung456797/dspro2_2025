import flet as ft 

def weather_card(date,weather,min_t,max_t):
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
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(f"{min_t}°C",color=ft.colors.BLUE),
                            ft.Text(" / "),
                            ft.Text(f"{max_t}°C",color=ft.colors.RED),
                        ],
                    ),
                ],
            ),
        ),
    )
    
def main(page: ft.Page):
    page.title = "天気予報(NavigationRail + ExpansionTile)"
    page.bgcolor = "#ECEFF1"
    page.window_width = 1000
    page.window_height = 650
    
    #天気カード表示領域
    forecast_area = ft.Column(scroll=ft.ScrollMode.AUTO,spacing=12)
    
    def show_sample_weather(e):
        forecast_area.controls.clear()
        sample_data = [
            ("11/1(月)","晴れ","20","28"),
            ("11/2(火)","曇り","22","27"),
            ("11/3(水)","雨のち曇り","19","24"),
            ("11/4(木)","晴れ時々曇り","21","29"),
            ("11/5(金)","雨","18","23"),
            ("11/6(土)","曇り一時雨","20","26"),
            ("11/7(日)","晴れ","22","30"),
        ]
        for data in sample_data:
            forecast_area.controls.append(weather_card(*data))
        page.update()
        
    # --------ナビゲーションレール---------
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=240,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.LOCATION_ON,
                label="地域一覧"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.INFO,
                label="アプリ情報"
            ),
        ],
    )
    
    # ExpansionTile リスク
    region_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("地域を選択",weight="bold",size=16),
            ft.Divider(tickness=1),
            ft.ExpansionTile(
                title=ft.Text("北海道地方"),
                children=[
                    ft.ListTile(
                        title=ft.Text("北海道"),
                        on_click=show_sample_weather,
                    ),
                ],
            ),
            ft.ExpansionTile(
                title=ft.Text("東北地方"),
                children=[
                    ft.ListTile(
                        title=ft.Text("青森県"),
                        on_click=show_sample_weather,
                    ),
                    ft.ListTile(
                        title=ft.Text("千葉県"),
                        on_click=show_sample_weather,
                    ),
                    ft.ListTile(
                        title=ft.Text("埼玉県"),
                        on_click=show_sample_weather,
                    ),
                ],
            ),
        ],
    )
    # --------レイアウト---------
    page.add(
        ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    width=280,
                    controls=[
                        nav,
                        ft.Container(height=1, bgcolor=ft.colors.GREY),
                        region_list,
                    ],
                ),
                ft.Container(
                    expand=True,
                    padding=20,
                    content=forecast_area,
                ),
            ],
        ),
    )

ft.app(target=main)