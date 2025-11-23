import flet as ft
from pages import *
from settings import *

def main(window: ft.Page):
    window.padding = 0
    window.title = "Не навреди"
    window.vertical_alignment = ft.MainAxisAlignment.START

    def route_change(views):
        window.views.clear()
        for page in PAGES:
            page = page(window)
            if window.route == page.route:
                window.views.append(page)

        window.update()

    def view_pop(event):
        window.views.pop()

    window.on_route_change = route_change
    window.on_view_pop = view_pop

    window.go("/authorization")
    
ft.app(main)