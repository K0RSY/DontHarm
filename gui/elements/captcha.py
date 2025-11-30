import flet as ft
from settings import *
from random import randint
import base64
import io
from PIL import Image

class Captcha(ft.Column):
    def __init__(self, window, on_change):
        self.window = window
        self.on_change = on_change

        self.value = False

        self.slider = ft.Slider(min=1, max=10, divisions=9, on_change=self.slider_changed, expand=True, width=300)

        self.correct_value = randint(1, 10)
        self.slider.value = randint(1, 10)
        while self.slider.value == self.correct_value:
            self.slider.value = randint(1, 10)
        
        self.image = ft.Image(expand=True, width=300)
        self.generate_image()

        self.content = [
            self.image,
            self.slider
        ]
        
        super().__init__(self.content, expand=True, alignment=ft.MainAxisAlignment.CENTER)

    def generate_image(self):
        img = Image.open("assets/images/captcha/bg.jpg")
        img = img.convert('RGBA')
        img_in = Image.open("assets/images/captcha/in.png")
        img_yan = Image.open("assets/images/captcha/yan.png")

        bg_size = img.size
        part_size = img_in.size

        x_padding = 30
        part_gaps = (bg_size[0] - x_padding * 2 - part_size[0] // 2) // 11
        y_padding = bg_size[1] // 2 - part_size[1] // 2

        img.paste(img_in, (x_padding + part_gaps * (int(self.slider.value) - 1), y_padding), mask=img_in)
        img.paste(img_yan, (x_padding + part_gaps * (int(self.correct_value) - 1), y_padding), mask=img_yan)
        
        buf = io.BytesIO()
        img.save(buf, format="png")
        buf.seek(0)
        img_bytes = buf.read()

        img.close()
        img_in.close()
        img_yan.close()

        self.image.src_base64 = base64.b64encode(img_bytes).decode()
        self.window.update()

    def slider_changed(self, event):
        self.value = self.slider.value == self.correct_value

        self.generate_image()

        self.window.update()

        self.on_change(None)
