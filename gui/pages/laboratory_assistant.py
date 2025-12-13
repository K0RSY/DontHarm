import flet as ft
from settings import *
import gui.elements.timer
import gui.elements.qrcode_scanner

class LaboratoryAssistant(ft.View):
    def __init__(self, window):
        self.window = window
        
        self.content = ft.Column(
            [
                gui.elements.timer.Timer(window),
                gui.elements.qrcode_scanner.QRCodeScanner(window),
            ]
        )

        super().__init__("/laboratory_assistant", [self.content], bgcolor=COLOR_BG)