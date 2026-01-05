import flet as ft
from settings import *
import gui.elements.check_generator

class Others(ft.View):
    def __init__(self, window):
        self.window = window
        
        self.content = gui.elements.check_generator.CheckGenerator(self.window)

        super().__init__("/others", [self.content], bgcolor=COLOR_BG)