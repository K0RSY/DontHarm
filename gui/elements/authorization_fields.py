import flet as ft
from settings import *
import gui.elements.captcha
import json
import datetime

class AuthorisationFields(ft.Row):
    def __init__(self, window):
        self.window = window

        self.login_field = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Логин")
        self.password_field = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Пароль", password=True)
        self.log_in_button = ft.Button("Войти", on_click=self.log_in, expand=True, bgcolor=COLOR_FG, color=COLOR_TEXT)
        self.captcha = gui.elements.captcha.Captcha(self.window, on_change=self.captcha_change)
        self.warning = ft.Text("Подождите перед тем как войти снова!", color=COLOR_TEXT, visible=False)
        
        self.content = [
            ft.Column(
                [
                    self.login_field,
                    self.password_field,
                    self.log_in_button,
                    self.captcha,
                    self.warning
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]

        self.is_human = False

        self.check_on_humanity()

        super().__init__(self.content, expand=True, alignment=ft.MainAxisAlignment.CENTER)

    def captcha_change(self, event):
        self.is_human = self.captcha.value
    
    def log_in(self, event):
        current_date = datetime.datetime.now()

        if current_date - self.last_fail_date < datetime.timedelta(seconds=TIMEOUT_DURATION):
            self.warning.visible = True
            self.window.update()
        else:
            self.warning.visible = False
            self.window.update()

            if self.login_field.value == LOGIN and self.password_field.value == PASSWORD and self.is_human:
                self.set_humanity()
                if ROLE == "laboratory_assistant":
                    self.window.go("/laboratory_assistant")
                else:
                    self.window.go("/others")
            else:
                self.destroy_humanity()
                self.check_on_humanity()

    def set_humanity(self):
        with open(USER_DATA_FILE, "r") as file:  
            user_data = json.load(file)

        user_data["is_human"] = True
        
        with open(USER_DATA_FILE, "w") as file:  
            user_data = json.dump(user_data, file)

    def destroy_humanity(self):
        with open(USER_DATA_FILE, "r") as file:  
            user_data = json.load(file)

        user_data["is_human"] = False
        user_data["last_fail_date"] = datetime.datetime.now().strftime(TIME_MASK)
        
        with open(USER_DATA_FILE, "w") as file:  
            user_data = json.dump(user_data, file)

    def check_on_humanity(self):
        with open(USER_DATA_FILE, "r") as file:  
            user_data = json.load(file)

        if user_data["is_human"]:
            self.is_human = True
            self.captcha.visible = False
            self.window.update()
        else:
            self.is_human = False
            self.captcha.visible = True
            self.window.update()

        self.last_fail_date = datetime.datetime.strptime(user_data["last_fail_date"], TIME_MASK)