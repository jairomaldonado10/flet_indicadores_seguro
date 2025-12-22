import flet as ft
from ecotech import Database, Auth
import os

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "EcoTech"
        self.db = Database(
            os.getenv("ORACLE_USER"),
            os.getenv("ORACLE_DSN"),
            os.getenv("ORACLE_PASSWORD")
        )
        self.show_login()

    def show_login(self):
        self.page.controls.clear()

        self.user = ft.TextField(label="Usuario")
        self.password = ft.TextField(label="Contraseña", password=True)
        self.msg = ft.Text()

        self.page.add(
            ft.Text("Login", size=22),
            self.user,
            self.password,
            ft.ElevatedButton("Ingresar", on_click=self.login),
            ft.TextButton("Registrarse", on_click=lambda e: self.show_register()),
            self.msg
        )
        self.page.update()

    def show_register(self):
        self.page.controls.clear()

        self.reg_id = ft.TextField(label="ID")
        self.reg_user = ft.TextField(label="Usuario")
        self.reg_pass = ft.TextField(label="Contraseña", password=True)
        self.msg = ft.Text()

        self.page.add(
            ft.Text("Registro", size=22),
            self.reg_id,
            self.reg_user,
            self.reg_pass,
            ft.ElevatedButton("Registrar", on_click=self.register),
            ft.TextButton("Volver", on_click=lambda e: self.show_login()),
            self.msg
        )
        self.page.update()

    def login(self, e):
        res = Auth.login(self.db, self.user.value, self.password.value)
        self.msg.value = res["message"]
        if res["success"]:
            self.show_menu()
        self.page.update()

    def register(self, e):
        res = Auth.register(
            self.db,
            int(self.reg_id.value),
            self.reg_user.value,
            self.reg_pass.value
        )
        self.msg.value = res["message"]
        self.page.update()

    def show_menu(self):
        self.page.controls.clear()
        self.page.add(
            ft.Text("Menú principal", size=22),
            ft.ElevatedButton("Salir", on_click=lambda e: self.show_login())
        )
        self.page.update()

if __name__ == "__main__":
    ft.app(target=App)
