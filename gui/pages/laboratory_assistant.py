import flet as ft
from settings import *
import gui.elements.timer

class LaboratoryAssistant(ft.View):
    def __init__(self, window):
        self.window = window
        
        self.content = gui.elements.timer.Timer(window)

        super().__init__("/laboratory_assistant", [self.content], bgcolor=COLOR_BG)