import flet as ft
from settings import *

class Others(ft.View):
    def __init__(self, window):
        self.window = window
        
        self.content = ft.Text("Вы не лаборант")

        super().__init__("/others", [self.content], bgcolor=COLOR_BG)