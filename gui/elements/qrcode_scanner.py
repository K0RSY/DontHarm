import flet as ft
from settings import *
from pyzbar.pyzbar import decode
from PIL import Image
from req.req import Req
import datetime

class QRCodeScanner(ft.Row):
    def __init__(self, window):
        self.window = window

        self.names_filed = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Фамилия Имя")
        self.code_field = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Коды (код-количество через запятую)")
        self.manual_insert = ft.Row(
            [
                self.names_filed,
                self.code_field
            ],
            expand=True
        )
        
        self.user_names = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Фамилия Имя Отчество")
        self.user_birth_date = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Дата рождения 'день.месяц.год'")
        self.user_passport_seria = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Серия паспорта")
        self.user_passport_number = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Номер паспорта")
        self.user_phone = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Телефон")
        self.user_email = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="E-mail")
        self.user_submit = ft.Button("Добавить", on_click=self.submit_user, expand=True, bgcolor=COLOR_FG, color=COLOR_TEXT)
        self.user_cancel = ft.Button("Отменить", on_click=self.cancel_user, expand=True, bgcolor=COLOR_FG, color=COLOR_TEXT)
        self.add_user_fields = ft.Column(
            [
                self.user_names,
                self.user_birth_date,
                ft.Row(
                    [
                        self.user_passport_seria,
                        self.user_passport_number
                    ]
                ),
                self.user_phone,
                self.user_email,
                ft.Row(
                    [
                        self.user_submit,
                        self.user_cancel
                    ]
                )
            ],
            expand=True,
            visible=False
        )

        self.select_file_button = ft.Button("Загрузить из QR-кода...", on_click=self.select_file, expand=True, bgcolor=COLOR_FG, color=COLOR_TEXT)
        self.submit_button = ft.Button("Отправить", on_click=self.submit, expand=True, bgcolor=COLOR_FG, color=COLOR_TEXT)
        self.file_selector = ft.FilePicker(on_result=self.show_result)
        self.warning = ft.Text("", color=COLOR_TEXT)
        self.add_user_button = ft.Button("Доавить пользователя...", on_click=self.add_user, expand=True, bgcolor=COLOR_FG, color=COLOR_TEXT, visible=False)

        self.content = [
            ft.Column(
                [
                    self.select_file_button,
                    self.manual_insert,
                    self.submit_button,
                    self.warning,
                    self.add_user_button,
                    self.add_user_fields,
                    self.file_selector
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]

        super().__init__(self.content, expand=True, alignment=ft.MainAxisAlignment.CENTER)

    def select_file(self, event):
        self.file_selector.pick_files("Выбрать QR-код", file_type=ft.FilePickerFileType.IMAGE)

    def show_result(self, event):
        if event.files == None:
            return 0
        
        img = Image.open(event.files[0].path)

        decoded_objects = decode(img)

        if decoded_objects:
            result = decoded_objects[0].data.decode('utf-8')

        result = [i.split("=")[1].strip() for i in result.split(";")]
        
        self.code_field.value = ",".join([f'{i["code"]}-{i["count"]}' for i in eval(result[1].replace("“", '"').replace("”", '"').replace("count", '"count"'))])

        self.names_filed.value = result[0]
        
        self.window.update()

    def submit(self, event):
        try:
            names = self.names_filed.value.split()
            codes = [i.split("-") for i in self.code_field.value.split(",")]

            client_id = Req.send_get_request(f"get_field/clients/id/surname/{names[1]}")

            if client_id is None:
                self.warning.value = "Пользователь не найден, хотите его добавить?"
                self.add_user_button.visible = True
                self.window.update()
                return 0
            
            service_ids = Req.send_get_request(f"get_column/services/id")
            
            self.warning.value = ""
            self.add_user_button.visible = False
            self.add_user_fields.visible = False
            for i in codes:
                if not int(i[0]) in service_ids:
                    self.warning.value += f"Не удалось добавить код {i[0]}, услуга не найдена\n" 
                    continue
                
                data = {
                    "serviceId": i[0],
                    "clientId": client_id
                }

                for _ in range(int(i[1])):
                    Req.send_post_request("submit_fields/orders", data)

                self.warning.value += f"Добавлен код {i[0]}, исполнено {i[1]} раз\n"
            self.window.update()
        except:
            self.warning.value = "Проверьте правильность заполнения полей"
            
            self.window.update()

    def add_user(self, event):
        self.warning.value = "Добавить пользователя..."
        self.add_user_fields.visible = True
        self.add_user_button.visible = False
        self.submit_button.visible = False

        self.window.update()

    def submit_user(self, event):
        try:
            date = datetime.datetime.strptime(self.user_birth_date.value, "%d.%m.%Y").date().strftime("%Y-%m-%d")

            data = {
                "name": self.user_names.value.split()[0],
                "surname": self.user_names.value.split()[1],
                "patronymic": self.user_names.value.split()[2],
                "dateOfBirth": date,
                "passportSeria": self.user_passport_seria.value,
                "passportNumber": self.user_passport_number.value,
                "phone": self.user_phone.value,
                "email": self.user_email.value
            }

            Req.send_post_request("submit_fields/clients", data)

            self.cancel_user(None)
            self.warning.value = "Пользователь добавлен успешно"
            self.add_user_button.visible = False
            self.window.update()
        except:
            self.warning.value = "Проверьте правильность заполнения полей"

            self.window.update()

    def cancel_user(self, event):
        self.warning.value = "Пользователь не найден, хотите его добавить?"
        self.add_user_button.visible = True
        self.add_user_fields.visible = False
        self.submit_button.visible = True
        
        self.window.update()