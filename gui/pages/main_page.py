import flet as ft
from settings import *
import gui.elements.authorization_fields

class MainPage(ft.View):
    def __init__(self, window):
        self.window = window
        
        self.content = ft.Column(
            [
                gui.elements.authorization_fields.AuthorisationFields(window)
            ],
            spacing=0
        )

        super().__init__("/", [self.content], bgcolor=COLOR_BG)