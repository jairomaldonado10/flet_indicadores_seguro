import flet as ft
from ecotech import Database, Auth, Finance, Consultas

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ecotech Solutions"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0f172a"
        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"
        self.page.padding = 20

        self.db = Database()
        self.user = None

        self.page_login()

    def card(self, title, controls):
        return ft.Container(
            width=420,
            padding=30,
            bgcolor="#111827",
            border_radius=16,
            border=ft.border.all(1, "#1f2937"),
            shadow=ft.BoxShadow(blur_radius=30, color="black"),
            content=ft.Column(
                spacing=18,
                horizontal_alignment="center",
                controls=[ft.Text(title, size=22, weight=ft.FontWeight.BOLD)] + controls
            )
        )

    def input(self, label, password=False):
        return ft.TextField(
            label=label,
            width=320,
            password=password,
            can_reveal_password=password,
            filled=True,
            bgcolor="#020617",
            border_radius=10
        )

    def button(self, text, action):
        return ft.ElevatedButton(
            text,
            width=320,
            height=44,
            on_click=action,
            style=ft.ButtonStyle(
                bgcolor="#2563eb",
                color="white",
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )

    def link(self, text, action):
        return ft.TextButton(text, on_click=action)

    def page_login(self):
        self.page.controls.clear()
        self.in_user = self.input("Nombre de usuario")
        self.in_pass = self.input("Contraseña", True)
        self.msg = ft.Text("", color="red")

        self.page.add(self.card("Ecotech Solutions", [
            self.in_user,
            self.in_pass,
            self.button("Iniciar sesión", self.handle_login),
            self.msg,
            self.link("Registrarse", lambda e: self.page_register())
        ]))
        self.page.update()

    def handle_login(self, e):
        if Auth.login(self.db, self.in_user.value, self.in_pass.value):
            self.user = self.in_user.value.strip().upper()
            self.page_menu()
        else:
            self.msg.value = "Credenciales inválidas"
            self.page.update()

    def page_register(self):
        self.page.controls.clear()
        self.in_id = self.input("ID de usuario")
        self.in_user = self.input("Nombre de usuario")
        self.in_pass = self.input("Contraseña", True)
        self.msg = ft.Text("", color="red")

        self.page.add(self.card("Registro", [
            self.in_id,
            self.in_user,
            self.in_pass,
            self.button("Registrarse", self.handle_register),
            self.msg,
            self.link("Volver", lambda e: self.page_login())
        ]))
        self.page.update()

    def handle_register(self, e):
        try:
            Auth.register(self.db, int(self.in_id.value), self.in_user.value, self.in_pass.value)
            self.msg.color = "green"
            self.msg.value = "Usuario registrado correctamente"
        except:
            self.msg.color = "red"
            self.msg.value = "Error al registrar"
        self.page.update()

    def page_menu(self):
        self.page.controls.clear()
        self.page.add(self.card(f"Bienvenido {self.user}", [
            self.button("Consultar indicador", lambda e: self.page_indicator()),
            self.button("Historial", lambda e: self.page_history()),
            self.link("Cerrar sesión", lambda e: self.page_login())
        ]))
        self.page.update()

    def page_indicator(self):
        self.page.controls.clear()
        self.dd = ft.Dropdown(
            width=320,
            value="uf",
            options=[ft.dropdown.Option(i) for i in ["uf", "dolar", "euro", "utm"]]
        )
        self.msg = ft.Text("")

        self.page.add(self.card("Indicadores Económicos", [
            self.dd,
            self.button("Consultar", self.handle_indicator),
            self.msg,
            self.link("Volver", lambda e: self.page_menu())
        ]))
        self.page.update()

    def handle_indicator(self, e):
        try:
            valor, fecha = Finance.get(self.dd.value)
            Consultas.guardar(self.db, self.user, self.dd.value.upper(), fecha, valor)
            self.msg.color = "white"
            self.msg.value = f"{self.dd.value.upper()} = {valor}"
        except Exception as err:
            self.msg.color = "red"
            self.msg.value = str(err)
        self.page.update()

    def page_history(self):
        self.page.controls.clear()
        rows = Consultas.historial(self.db, self.user)
        items = [ft.Text(f"{r[0]} | {r[1]} | {r[2]}") for r in rows]
        if not items:
            items.append(ft.Text("Sin registros"))

        self.page.add(self.card("Historial", items + [
            self.link("Volver", lambda e: self.page_menu())
        ]))
        self.page.update()

def main(page: ft.Page):
    App(page)

ft.app(target=main)
