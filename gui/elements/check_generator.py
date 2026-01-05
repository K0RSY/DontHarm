import flet as ft
from settings import *
import datetime
from fpdf import FPDF
from req.req import *

class CheckGenerator(ft.Row):
    def __init__(self, window):
        self.window = window

        self.names_field = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Имя Фамилия")
        self.payement_time_field = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Срок для оплаты (дней)",  keyboard_type=ft.KeyboardType.NUMBER)
        self.start_field = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Начало счёта 'день.месяц.год'")
        self.end_field = ft.TextField(border_color=COLOR_TEXT, color=COLOR_TEXT, label="Конец счёта 'день.месяц.год'")

        self.submit_button = ft.Button("Сгенерировать", on_click=self.generate, bgcolor=COLOR_FG, color=COLOR_TEXT)

        self.warning = ft.Text("", color=COLOR_TEXT)

        self.start_field.value = datetime.datetime.now().strftime("%d.%m.%Y")
        self.end_field.value = self.start_field.value
        
        self.content = [
            ft.Column(
                [
                    self.names_field,
                    self.payement_time_field,
                    ft.Row(
                        [
                            self.start_field,
                            self.end_field
                        ]
                    ),
                    self.submit_button,
                    self.warning
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]

        super().__init__(self.content, expand=True, alignment=ft.MainAxisAlignment.CENTER)

    def generate(self, event):
        self.warning.value = ""

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            client_id = Req.send_get_request(f"get_field/clients/id/surname/{self.names_field.value.split()[1]}")

            start_date = datetime.datetime.strptime(self.start_field.value, "%d.%m.%Y")
            end_date = datetime.datetime.strptime(self.end_field.value, "%d.%m.%Y")

            orders_raw = [Req.send_get_request(f"get_column/orders/date"), Req.send_get_request(f"get_column/orders/serviceId"), Req.send_get_request(f"get_column/orders/clientId")]
            orders = [[], []]

            for order_index in range(len(orders_raw[0])):
                date = datetime.datetime.strptime(orders_raw[0][order_index], "%Y-%m-%d")

                if start_date <= date <= end_date and orders_raw[2][order_index] == client_id:
                    orders[0].append(orders_raw[1][order_index])
                    orders[1].append(Req.send_get_request(f"get_field/services/cost/id/{orders_raw[1][order_index]}"))
            
            text = []
            text.append(f"Names: {self.names_field.value}")
            text.append(f"Phone number: {Req.send_get_request('get_field/clients/phone/id/' + str(client_id))}")
            text.append("")
            text.append(f"Payment time: {self.payement_time_field.value} days")
            text.append("")
            text.append(f"Service codes: {', '.join(map(str, orders[0]))}")
            text.append(f"Service costs: {', '.join(map(str, orders[1]))}")
            text.append(f"Full price: {round(sum(orders[1]), 2)}")

            for i in range(len(text)):
                pdf.cell(0, 5, text[i], new_x="LMARGIN", new_y="NEXT")

            pdf.output(CHECK_FILE_NAME + ".pdf")
        except Exception as e:
            print(e)
            self.warning.value = "Проверьте правильность заполнения полей"
        
        self.window.update()