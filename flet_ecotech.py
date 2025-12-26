import flet as ft
from ecotech import Database, Auth, Finance, Consultas

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ecotech Solutions"
        self.page.bgcolor = "#0F172A"
        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"

        self.db = Database()
        self.user = None

        self.login()

    def shadow_button(self, text, on_click, color):
        return ft.Container(
            width=420,
            height=50,
            border_radius=16,
            bgcolor=color,
            shadow=ft.BoxShadow(
                blur_radius=18,
                spread_radius=1,
                color="#00000088",
                offset=ft.Offset(0, 6)
            ),
            content=ft.TextButton(
                text=text,
                on_click=on_click,
                style=ft.ButtonStyle(
                    color="black",
                    text_style=ft.TextStyle(
                        size=16,
                        weight="bold"
                    )
                )
            )
        )

    def card(self, controls):
        return ft.Container(
            width=520,
            padding=36,
            bgcolor="#111827",
            border_radius=22,
            shadow=ft.BoxShadow(
                blur_radius=30,
                color="#000000AA",
                offset=ft.Offset(0, 10)
            ),
            content=ft.Column(
                horizontal_alignment="center",
                spacing=20,
                controls=controls
            )
        )

    def login(self):
        self.page.clean()

        self.in_user = ft.TextField(
            label="Nombre de usuario",
            width=420,
            bgcolor="#1F2933",
            border_radius=14
        )

        self.in_pass = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=420,
            bgcolor="#1F2933",
            border_radius=14
        )

        self.msg = ft.Text("", color="#EF4444")

        self.page.add(self.card([
            ft.Text("Ecotech Solutions", size=34, weight="bold"),
            ft.Text("Plataforma de indicadores económicos", color="#94A3B8"),
            self.in_user,
            self.in_pass,
            self.shadow_button(
                "Iniciar sesión",
                self.do_login,
                "#22D3EE"
            ),
            self.msg,
            ft.TextButton(
                "Registrarse",
                on_click=lambda e: self.register(),
                style=ft.ButtonStyle(color="#38BDF8")
            )
        ]))

    def do_login(self, e):
        if Auth.login(self.db, self.in_user.value, self.in_pass.value):
            self.user = self.in_user.value
            self.menu()
        else:
            self.msg.value = "Credenciales inválidas"
            self.page.update()

    def register(self):
        self.page.clean()

        self.in_id = ft.TextField(label="ID", width=420, bgcolor="#1F2933", border_radius=14)
        self.in_user = ft.TextField(label="Usuario", width=420, bgcolor="#1F2933", border_radius=14)
        self.in_pass = ft.TextField(label="Contraseña", password=True, width=420, bgcolor="#1F2933", border_radius=14)

        self.msg = ft.Text("", color="#EF4444")

        self.page.add(self.card([
            ft.Text("Registro de usuario", size=28, weight="bold"),
            self.in_id,
            self.in_user,
            self.in_pass,
            self.shadow_button("Registrar", self.do_register, "#38BDF8"),
            self.msg,
            ft.TextButton("Volver", on_click=lambda e: self.login(), style=ft.ButtonStyle(color="#94A3B8"))
        ]))

    def do_register(self, e):
        try:
            Auth.register(self.db, int(self.in_id.value), self.in_user.value, self.in_pass.value)
            self.msg.color = "#22C55E"
            self.msg.value = "Usuario registrado correctamente"
        except Exception as ex:
            self.msg.color = "#EF4444"
            self.msg.value = str(ex)
        self.page.update()

    def menu(self):
        self.page.clean()

        self.page.add(self.card([
            ft.Text(f"Bienvenido {self.user}", size=26, weight="bold"),
            self.shadow_button("Consultar indicador", lambda e: self.indicators(), "#22D3EE"),
            self.shadow_button("Historial", lambda e: self.history(), "#38BDF8"),
            self.shadow_button("Cerrar sesión", lambda e: self.login(), "#F87171")
        ]))

    def indicators(self):
        self.page.clean()

        self.dd = ft.Dropdown(
            width=420,
            value="uf",
            options=[ft.dropdown.Option(i) for i in ["uf", "dolar", "euro", "utm"]],
            bgcolor="#1F2933",
            border_radius=14
        )

        self.msg = ft.Text("")

        self.page.add(self.card([
            ft.Text("Indicadores económicos", size=26, weight="bold"),
            self.dd,
            self.shadow_button("Consultar", self.do_indicator, "#22D3EE"),
            self.msg,
            ft.TextButton("Volver", on_click=lambda e: self.menu(), style=ft.ButtonStyle(color="#94A3B8"))
        ]))

    def do_indicator(self, e):
        try:
            value, _ = Finance.get(self.dd.value)
            Consultas.save(self.db, self.user, self.dd.value.upper(), value)
            self.msg.color = "#22C55E"
            self.msg.value = f"{self.dd.value.upper()} = {value}"
        except:
            self.msg.color = "#EF4444"
            self.msg.value = "Error al consultar indicador"
        self.page.update()

    def history(self):
        self.page.clean()

        rows = Consultas.history(self.db, self.user)
        col = ft.Column(scroll="auto", spacing=10)

        for r in rows:
            col.controls.append(
                ft.Container(
                    padding=12,
                    bgcolor="#1F2933",
                    border_radius=14,
                    content=ft.Text(f"{r[0]} | {r[1]} | {r[2]}")
                )
            )

        self.page.add(self.card([
            ft.Text("Historial de consultas", size=26, weight="bold"),
            col,
            ft.TextButton("Volver", on_click=lambda e: self.menu(), style=ft.ButtonStyle(color="#94A3B8"))
        ]))

def main(page: ft.Page):
    App(page)

ft.app(target=main)
