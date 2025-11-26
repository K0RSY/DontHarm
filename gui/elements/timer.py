import flet as ft
from settings import *
import threading
import time

class Timer(ft.Text):
    def __init__(self, window):
        self.window = window

        self.seconds = LABORATORY_ASSISTANT_SESSION_SECONDS

        self.message = ""

        super().__init__(value="")

        if self.window.route == "/laboratory_assistant":
            self.thread = threading.Thread(target=self.ticking)
            self.thread.start() 

    def ticking(self):
        while self.seconds > 0:
            self.tick()
            time.sleep(1)

        self.window.window.close()

    def tick(self):
        self.seconds -= 1

        if self.seconds == LABORATORY_ASSISTANT_SESSION_WARNING_SECONDS:
            self.message = "Скоро время закончится!"

        self.update()

    def format_time(self, seconds):
        result = f"{self.message} {(seconds // 60) // 60}:{(seconds // 60) % 60}:{seconds % 60}"

        return result

    def update(self):
        self.value = self.format_time(self.seconds)

        self.window.update()