import flet as ft
from settings import *
import gui.elements.authorization_fields

class Authorisation(ft.View):
    def __init__(self, window):
        self.window = window
        
        self.content = gui.elements.authorization_fields.AuthorisationFields(window)

        super().__init__("/authorization", [self.content], bgcolor=COLOR_BG)