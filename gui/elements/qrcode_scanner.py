import flet as ft
from settings import *
from pyzbar.pyzbar import decode
from PIL import Image

class QRCodeScanner(ft.Row):
    def __init__(self, window):
        self.window = window

        self.text = ft.Text("Результат чтения QR-кода будет отображён тут")
        self.select_file_button = ft.Button("Открыть файл", on_click=self.select_file, expand=True, bgcolor=COLOR_FG, color=COLOR_TEXT)
        self.file_selector = ft.FilePicker(on_result=self.show_result)

        self.content = [
            ft.Column(
                [
                    self.select_file_button,
                    self.text,
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

        self.text.value = result
        
        