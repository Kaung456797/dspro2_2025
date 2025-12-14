import flet
from flet import (
    Page,
    Row,
    Column,
    Container,
    ElevatedButton,
    Text,
    alignment,
    colors,
    border_radius,
    padding,
    margin,
    IconButton,
)

# シンプルな電卓ロジックを持つ Flet アプリ
def main(page: Page):
    page.title = "Calc App"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_width = 360
    page.window_height = 520
    page.bgcolor = colors.WHITE

    # 表示用テキスト
    display = Text("0", size=28, weight="bold", color=colors.WHITE)

    # 内部状態
    state = {
        "current": "0",      # 表示中の文字列
        "operand": None,     # 左オペランド（float）
        "operator": None,    # '+','-','*','/'
        "reset_next": False, # 次の数字入力で表示をリセットするか
    }

    def format_number(x):
        # 小数点 .0 を消す表示整形
        if x is None:
            return "0"
        if float(x).is_integer():
            return str(int(float(x)))
        else:
            # 小数点以下の不要なゼロを削る
            s = ("{:.10f}".format(float(x))).rstrip("0").rstrip(".")
            return s if s != "" else "0"

    def update_display():
        display.value = state["current"]
        display.update()

    def apply_operator(op):
        try:
            cur = float(state["current"])
        except:
            cur = 0.0

        if state["operand"] is None:
            state["operand"] = cur
        else:
            # 既存の operand と operator があれば計算
            if state["operator"] is not None:
                a = state["operand"]
                b = cur
                try:
                    if state["operator"] == "+":
                        res = a + b
                    elif state["operator"] == "-":
                        res = a - b
                    elif state["operator"] == "*":
                        res = a * b
                    elif state["operator"] == "/":
                        res = a / b
                    else:
                        res = b
                except Exception:
                    res = 0.0
                state["operand"] = res
                state["current"] = format_number(res)
        state["operator"] = op
        state["reset_next"] = True
        update_display()

    def on_button_click(e):
        btn = e.control.data  # ボタンのデータを利用
        # 数字ボタン
        if btn in [str(i) for i in range(10)]:
            if state["reset_next"] or state["current"] == "0":
                state["current"] = btn
                state["reset_next"] = False
            else:
                state["current"] += btn
            update_display()
            return

        # 小数点
        if btn == ".":
            if state["reset_next"]:
                state["current"] = "0."
                state["reset_next"] = False
            elif "." not in state["current"]:
                state["current"] += "."
            update_display()
            return

        # 全消去
        if btn == "AC":
            state["current"] = "0"
            state["operand"] = None
            state["operator"] = None
            state["reset_next"] = False
            update_display()
            return

        # 符号反転
        if btn == "+/-":
            try:
                val = float(state["current"])
                val = -val
                state["current"] = format_number(val)
            except:
                state["current"] = "0"
            update_display()
            return

        # パーセント
        if btn == "%":
            try:
                val = float(state["current"]) / 100.0
                state["current"] = format_number(val)
            except:
                state["current"] = "0"
            update_display()
            return

        # 演算子
        if btn in ["/", "*", "-", "+"]:
            apply_operator(btn)
            return

        # イコール
        if btn == "=":
            if state["operator"] is not None:
                apply_operator(None)  # 既存 operator を適用（apply_operator は operator を上書きするので先に保存）
                # apply_operator(None) の実装上 operator が None となってしまうため、実際の計算を直接行う:
                try:
                    b = float(state["current"])
                except:
                    b = 0.0
                a = state["operand"] if state["operand"] is not None else 0.0
                op = state["operator"]
                # NOTE: 上で operator を None にしてしまう問題回避としてここで再計算する:
                # （より簡潔にするため、簡単に再計算）
                # 実装：上の apply_operator 呼び出しを行わず、ここで計算するほうが安全
                # なので修正: 再計算を行う
                # 実際には以下の分岐で計算する
                if state["operator"] is None:
                    # apply_operator(None) によって operator が None になっているケースがあるため、
                    # 代わりに最後に押された演算子を使って計算するロジックは上の apply_operator を使わない方が良い。
                    pass

            # 安全にイコールを実行する別実装:
            try:
                if state["operator"] is not None and state["operand"] is not None:
                    a = state["operand"]
                    b = float(state["current"])
                    if state["operator"] == "+":
                        res = a + b
                    elif state["operator"] == "-":
                        res = a - b
                    elif state["operator"] == "*":
                        res = a * b
                    elif state["operator"] == "/":
                        res = a / b
                    else:
                        res = b
                    state["current"] = format_number(res)
                    state["operand"] = None
                    state["operator"] = None
                    state["reset_next"] = True
                # 何もなければそのまま
            except Exception:
                state["current"] = "0"
                state["operand"] = None
                state["operator"] = None
                state["reset_next"] = True
            update_display()
            return

    # ボタン生成ユーティリティ
    def make_btn(label, width=70, height=56, bg=colors.GREY_800, fg=colors.WHITE, radius=28):
        btn = ElevatedButton(
            label,
            data=label,
            on_click=on_button_click,
            style={"padding": 0},
            height=height,
            width=width,
        )
        # Container で装飾して丸める
        c = Container(
            content=btn,
            padding=padding.all(0),
            alignment=alignment.center,
            border_radius=border_radius.all(radius),
            bgcolor=bg,
            margin=margin.all(6),
        )
        # ボタン自身の見た目はOS依存なので container でラップ
        # データは inner button に remain するため .data で受け取れる
        return c

    # レイアウト: 画面上は黒い丸角パネルの中に表示とボタン群
    panel = Container(
        content=Column(
            [
                # 上部表示領域（右寄せ）
                Container(
                    content=display,
                    alignment=alignment.center_right,
                    padding=padding.only(right=18, top=18, bottom=8),
                ),
                # ボタン群（行ごと）
                Column(
                    [
                        Row(
                            [
                                make_btn("AC", 64, 48, bg=colors.GREY_300, fg=colors.BLACK),
                                make_btn("+/-", 64, 48, bg=colors.GREY_300, fg=colors.BLACK),
                                make_btn("%", 64, 48, bg=colors.GREY_300, fg=colors.BLACK),
                                make_btn("/", 64, 48, bg=colors.ORANGE_700, fg=colors.WHITE),
                            ],
                            alignment="spaceBetween",
                        ),
                        Row(
                            [
                                make_btn("7"),
                                make_btn("8"),
                                make_btn("9"),
                                make_btn("*", bg=colors.ORANGE_700),
                            ],
                            alignment="spaceBetween",
                        ),
                        Row(
                            [
                                make_btn("4"),
                                make_btn("5"),
                                make_btn("6"),
                                make_btn("-", bg=colors.ORANGE_700),
                            ],
                            alignment="spaceBetween",
                        ),
                        Row(
                            [
                                make_btn("1"),
                                make_btn("2"),
                                make_btn("3"),
                                make_btn("+", bg=colors.ORANGE_700),
                            ],
                            alignment="spaceBetween",
                        ),
                        Row(
                            [
                                # 0 は幅を広く
                                Container(
                                    content=ElevatedButton("0", data="0", on_click=on_button_click, style={"padding": 0}),
                                    padding=padding.all(0),
                                    alignment=alignment.center,
                                    border_radius=border_radius.all(28),
                                    bgcolor=colors.GREY_800,
                                    margin=margin.all(6),
                                    width=150,
                                    height=56,
                                ),
                                make_btn("."),
                                make_btn("=", bg=colors.ORANGE_700),
                            ],
                            alignment="spaceBetween",
                        ),
                    ]
                ),
            ],
            tight=True,
            spacing=6,
        ),
        padding=padding.only(top=8, left=12, right=12, bottom=18),
        width=320,
        height=420,
        border_radius=border_radius.all(24),
        bgcolor=colors.BLACK,
        alignment=alignment.center,
    )

    # 外側コンテナ（背景に余白や影をつけたい場合ここで調整）
    outer = Container(
        content=panel,
        padding=padding.all(12),
    )

    page.add(outer)
    update_display()


if __name__ == "__main__":
    flet.app(target=main)