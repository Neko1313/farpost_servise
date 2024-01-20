import flet as ft
import requests

import importlib
from typing import Union
from time import sleep
from uuid import UUID
from lxml import html
from datetime import time

from const.const import RequstsApi
from components.abs_class import ContentAbstract, PagesAbstract, AlertDialogInput


class ViewData(ContentAbstract):
    """
    Страница просмотра записей
    """

    def __init__(self, page: ft.Page, master: PagesAbstract):
        self.master = master
        self.page = page

        if isinstance(self.master.headers_cookies, dict) and "cookies" in self.master.headers_cookies:
            cookies = self.master.headers_cookies["cookies"]
            self.login: str = ""
            if isinstance(cookies, dict):
                self.login = cookies.get("login")
            else:
                self.login = ""
                self.out(1)
        else:
            self.login = ""
            self.out(1)

        telegram_chat_id = requests.get(RequstsApi.GetTg.value + self.login).json()["telegram_id"]
        if telegram_chat_id:
            self.telegram_chat_id = ft.TextField(label="Ваш chat_id : " + str(telegram_chat_id))
        else:
            self.telegram_chat_id = ft.TextField(label="Введите свой chat_id")

        self.dlg: AlertDialogInput = AlertDialogInput()

        self.tab_settings_content = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        [
                            ft.Row(
                                controls=[
                                    ft.Text(value=f"Логин : " + self.login, size=17),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                controls=[
                                    ft.TextButton(text="Где взять", on_click=self.open_video),
                                    self.telegram_chat_id,
                                    ft.TextButton(text="Обновить", on_click=self.update_tg),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(text="Выйти", on_click=self.out),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )

        self.tab_all_content = ft.Container(
            content=ft.Row(
                [
                    ft.Column(),
                    ft.Column(
                        [
                            ft.DataTable(
                                data_row_min_height=50,
                                data_row_max_height=100,
                                columns=[
                                    ft.DataColumn(ft.Text("Настройки")),
                                    ft.DataColumn(ft.Text("Название")),
                                    ft.DataColumn(ft.Text("Город")),
                                    ft.DataColumn(ft.Text("Категория")),
                                    ft.DataColumn(ft.Text("Подкатегория")),
                                    ft.DataColumn(ft.Text("Изображение")),
                                ],
                                rows=[
                                    self.creact_row(i, "All")
                                    for i in requests.get(
                                        RequstsApi.Items.value + f"""?user_login={self.login}"""
                                    ).json()
                                ],
                            ),
                        ],
                        height=600,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    ft.Column(
                        [ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda e: self.update_data(e, 1))],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )

        self.tab_histore_content = ft.Container(
            content=ft.Row(
                [
                    ft.Column(),
                    ft.Column(
                        [
                            ft.DataTable(
                                data_row_min_height=50,
                                data_row_max_height=100,
                                columns=[
                                    ft.DataColumn(ft.Text("Название")),
                                    ft.DataColumn(ft.Text("Город")),
                                    ft.DataColumn(ft.Text("Подкатегория")),
                                    ft.DataColumn(ft.Text("id объявления")),
                                    ft.DataColumn(ft.Text("Закрепленая позиция")),
                                    ft.DataColumn(ft.Text("Лимит цены")),
                                    ft.DataColumn(ft.Text("Дата начала")),
                                    ft.DataColumn(ft.Text("Дата конца")),
                                ],
                                rows=[
                                    self.creact_row(i, "histore")
                                    for i in requests.get(
                                        RequstsApi.AbsActiveWithUserNotNone.value + f"""?user_login={self.login}"""
                                    ).json()
                                ],
                            ),
                        ],
                        height=600,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    ft.Column(
                        [ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda e: self.update_data(e, 2))],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )

        self.tab_active_content = ft.Container(
            content=ft.Row(
                [
                    ft.Column(),
                    ft.Column(
                        [
                            ft.DataTable(
                                data_row_min_height=50,
                                data_row_max_height=100,
                                columns=[
                                    ft.DataColumn(ft.Text("Закрыть активность")),
                                    ft.DataColumn(ft.Text("Название")),
                                    ft.DataColumn(ft.Text("Город")),
                                    ft.DataColumn(ft.Text("Подкатегория")),
                                    ft.DataColumn(ft.Text("id объявления")),
                                    ft.DataColumn(ft.Text("Закрепленая позиция")),
                                    ft.DataColumn(ft.Text("Лимит цены")),
                                    ft.DataColumn(ft.Text("Дата начала")),
                                    ft.DataColumn(ft.Text("Дата конца")),
                                ],
                                rows=[
                                    self.creact_row(i, "active")
                                    for i in requests.get(
                                        RequstsApi.AbsActiveWithUser.value + f"""?user_login={self.login}"""
                                    ).json()
                                ],
                            ),
                        ],
                        height=600,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    ft.Column(
                        [ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda e: self.update_data(e, 3))],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )

        self.tab_menu = ft.Tabs(
            selected_index=1,
            animation_duration=300,
            tabs=[
                ft.Tab(icon=ft.icons.SETTINGS, content=self.tab_settings_content),
                ft.Tab(text="Все", content=self.tab_all_content),
                ft.Tab(text="История", content=self.tab_histore_content),
                ft.Tab(text="Активные", content=self.tab_active_content),
            ],
            expand=1,
        )
        
        wallet_value: str = str(requests.get(RequstsApi.Wallet.value + self.login).json()["wallet"])
        self.wallet_value = ft.Text(value=wallet_value, size=15)
        self.wallet = ft.Row(
            controls=[self.wallet_value, ft.IconButton(icon=ft.icons.AUTORENEW, on_click=self.update_wallet)]
        )
        
        self.time_picker_start = ft.TimePicker(
            confirm_text="Подтвердить",
            error_invalid_text="Time out of range",
            help_text="Выберите время от",
            on_change=self.change_time_start,
            cancel_text="Отменить",
            time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
            hour_label_text="Часы",
            minute_label_text="Минуты"
        )
        self.time_picker_end = ft.TimePicker(
            confirm_text="Подтвердить",
            error_invalid_text="Time out of range",
            help_text="Выберите время до",
            on_change=self.change_time_end,
            cancel_text="Отменить",
            time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
            hour_label_text="Часы",
            minute_label_text="Минуты"
        )
        
        self.page.add(self.wallet)
        self.page.add(self.tab_menu)
        
    def change_time_start(self,e):
        self.time_start = time(hour=self.time_picker_start.value.hour, minute=self.time_picker_start.value.minute)
    
    def change_time_end(self,e):
        self.time_end = time(hour=self.time_picker_end.value.hour, minute=self.time_picker_end.value.minute)
        
    def open_time_start(self, e):
        self.page.add(self.time_picker_start)
        self.time_picker_start.open = True
        self.time_picker_start.update()

    def open_time_end(self, e):
        self.page.add(self.time_picker_end)
        self.time_picker_end.open = True
        self.time_picker_end.update()
        

    def update_tg(self, e):
        tg_chat_id = self.telegram_chat_id.value
        requests.get(RequstsApi.UpdataTg.value + f"login={self.login}&tg_chat_id={tg_chat_id}")
        telegram_chat_id = requests.get(RequstsApi.GetTg.value + self.login).json()["telegram_id"]
        self.telegram_chat_id.label = "Ваш chat_id : " + str(telegram_chat_id)

        self.page.update()
    
    def open_video(self, e):
        self.page.launch_url('https://lumpics.ru/how-find-out-chat-id-in-telegram/')

    def creact_row(self, data_row: dict, tab_name: str) -> ft.DataRow:
        """
        Создание данных в нутри таблицы
        """

        if not isinstance(data_row, dict):
            print(f"Неправильный тип данных: {type(data_row)}")
            return ft.DataRow(cells=[])

        if tab_name == "All":
            return ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.PENDING_ACTIONS_ROUNDED,
                            on_click=lambda e: self.open_dialog(e, data_row["abs_id"]),
                        )
                    ),
                    ft.DataCell(ft.Text(data_row["name_farpost"])),
                    ft.DataCell(ft.Text(data_row["city_english"])),
                    ft.DataCell(ft.Text(data_row["categore"])),
                    ft.DataCell(ft.Text(data_row["subcategories"])),
                    ft.DataCell(
                        ft.Image(
                            src=data_row["link_main_img"],
                        )
                    ),
                ],
            )
        elif tab_name == "histore":
            return ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(data_row["name_farpost"])),
                    ft.DataCell(ft.Text(data_row["city_english"])),
                    ft.DataCell(ft.Text(data_row["subcategories"])),
                    ft.DataCell(ft.Text(data_row["abs_id"])),
                    ft.DataCell(ft.Text(data_row["position"])),
                    ft.DataCell(ft.Text(data_row["price_limitation"])),
                    ft.DataCell(ft.Text(data_row["date_creation"])),
                    ft.DataCell(ft.Text(data_row["date_closing"])),
                ],
            )

        elif tab_name == "active":
            return ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e: self.open_dialog_confirmation(e, data_row["abs_active_id"]),
                        )
                    ),
                    ft.DataCell(ft.Text(data_row["name_farpost"])),
                    ft.DataCell(ft.Text(data_row["city_english"])),
                    ft.DataCell(ft.Text(data_row["subcategories"])),
                    ft.DataCell(ft.Text(data_row["abs_id"])),
                    ft.DataCell(ft.Text(data_row["position"])),
                    ft.DataCell(ft.Text(data_row["price_limitation"])),
                    ft.DataCell(ft.Text(data_row["date_creation"])),
                    ft.DataCell(ft.Text(data_row["date_closing"])),
                ],
            )

    def out(self, e) -> None:
        """
        Метод для выхода в авторизацию
        """

        login = importlib.import_module("components.login")
        self.master.headers_cookies = None
        self.master.new_win(login.Login)

    def update_wallet(self, e) -> None:
        wallet_value: str = str(requests.get(RequstsApi.Wallet.value + self.login).json()["wallet"])
        self.wallet_value.value = wallet_value

        self.page.update()

    def update_data(self, e, tab_index: int) -> None:
        """
        Запрос на обновление
        """
        if tab_index == 1:
            self.tab_all_content.content = ft.Row(
                [
                    ft.Column(),
                    ft.Column(
                        [
                            ft.DataTable(
                                data_row_min_height=50,
                                data_row_max_height=100,
                                columns=[
                                    ft.DataColumn(ft.Text("Настройки")),
                                    ft.DataColumn(ft.Text("Название")),
                                    ft.DataColumn(ft.Text("Город")),
                                    ft.DataColumn(ft.Text("Категория")),
                                    ft.DataColumn(ft.Text("Подкатегория")),
                                    ft.DataColumn(ft.Text("Изображение")),
                                ],
                                rows=[
                                    self.creact_row(i, "All")
                                    for i in requests.post(
                                        RequstsApi.Updata.value + f"""?user_login={self.login}""",
                                        json=self.master.headers_cookies
                                    ).json()
                                ],
                            ),
                        ],
                        height=600,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    ft.Column(
                        [ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda e: self.update_data(e, 1))],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

        elif tab_index == 2:
            self.tab_histore_content.content = ft.Row(
                [
                    ft.Column(),
                    ft.Column(
                        [
                            ft.DataTable(
                                data_row_min_height=50,
                                data_row_max_height=100,
                                columns=[
                                    ft.DataColumn(ft.Text("Название")),
                                    ft.DataColumn(ft.Text("Город")),
                                    ft.DataColumn(ft.Text("Подкатегория")),
                                    ft.DataColumn(ft.Text("id объявления")),
                                    ft.DataColumn(ft.Text("Закрепленая позиция")),
                                    ft.DataColumn(ft.Text("Лимит цены")),
                                    ft.DataColumn(ft.Text("Дата начала")),
                                    ft.DataColumn(ft.Text("Дата конца")),
                                ],
                                rows=[
                                    self.creact_row(i, "histore")
                                    for i in requests.get(
                                        RequstsApi.AbsActiveWithUserNotNone.value + f"""?user_login={self.login}"""
                                    ).json()
                                ],
                            ),
                        ],
                        height=600,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    ft.Column(
                        [ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda e: self.update_data(e, 2))],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

        elif tab_index == 3:
            self.tab_active_content.content = ft.Row(
                [
                    ft.Column(),
                    ft.Column(
                        [
                            ft.DataTable(
                                data_row_min_height=50,
                                data_row_max_height=100,
                                columns=[
                                    ft.DataColumn(ft.Text("Закрыть активность")),
                                    ft.DataColumn(ft.Text("Название")),
                                    ft.DataColumn(ft.Text("Город")),
                                    ft.DataColumn(ft.Text("Подкатегория")),
                                    ft.DataColumn(ft.Text("id объявления")),
                                    ft.DataColumn(ft.Text("Закрепленая позиция")),
                                    ft.DataColumn(ft.Text("Лимит цены")),
                                    ft.DataColumn(ft.Text("Дата начала")),
                                    ft.DataColumn(ft.Text("Дата конца")),
                                ],
                                rows=[
                                    self.creact_row(i, "active")
                                    for i in requests.get(
                                        RequstsApi.AbsActiveWithUser.value + f"""?user_login={self.login}"""
                                    ).json()
                                ],
                            ),
                        ],
                        height=600,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    ft.Column(
                        [ft.IconButton(icon=ft.icons.AUTORENEW, on_click=lambda e: self.update_data(e, 3))],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

        self.page.update()

    def open_dialog_confirmation(self, e, abs_id) -> None:
        self.dlg = AlertDialogInput(
            abs_id=abs_id,
            title=ft.Text(f"Подтвертите что хотите отменить активность записи {abs_id}"),
            modal=True,
            actions=[
                ft.TextButton("Прекратить", on_click=lambda e: self.close_active(e, abs_id)),
                ft.TextButton("Отменить", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def get_top_one(self, abs_id) -> float:
        abs = requests.get(RequstsApi.AbsInfo.value + str(abs_id)).json()
        html_code = requests.get(
            f"https://www.farpost.ru/" + abs["category_attribute"],
            cookies=self.master.headers_cookies["cookies"],
            headers=self.master.headers_cookies["headers"],
        ).text

        html_parce = html.fromstring(html_code)

        list_item_price: list[float] = [
            float(i.split(":")[1].split("-")[0][2:])
            for i in html_parce.xpath(
                """//*[contains(concat( " ", @class, " " ), concat( " ", "bull-item__image-cell", " " ))]/@data-order-key"""
            )
        ]
        if len(list_item_price) > 0:
            if list_item_price[0] > 10000:
                return 10
            else:
                return list_item_price[0]
        else:
            return 10

    def open_dialog(self, e, abs_id) -> None:
        """Создание окна для сбора параметров"""

        price = self.get_top_one(abs_id)
        
        date_button_start = ft.ElevatedButton(
            "Время от",
            icon=ft.icons.TIME_TO_LEAVE,
            on_click=self.open_time_start,
        )
        date_button_end = ft.ElevatedButton(
            "Время до",
            icon=ft.icons.TIME_TO_LEAVE,
            on_click=self.open_time_end,
        )
        self.dlg = AlertDialogInput(
            abs_id=abs_id,
            modal=True,
            content=ft.Column(
                controls=[
                    ft.TextField(
                        label="Позиция",
                        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
                    ),
                    ft.TextField(
                        label="Лимит",
                        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
                    ),
                    ft.Text(
                        f"""Цена за 1 место сейчас : {price}\nРекамендуется ставить лимит в 2 раза больше чем цена за первое место
                        """,
                        size=20,
                    ),
                    ft.Row(
                        [
                            date_button_start,
                            date_button_end,
                        ],
                    ),
                ],
                width=600,
                height=300,
            ),
            actions=[
                ft.TextButton("Начать", on_click=self.creact_active),
                ft.TextButton("Отменить", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def close_dlg(self, e) -> None:
        """Закрыть диалоговое окно"""

        self.dlg.open = False
        self.page.update()

    def creact_active(self, e) -> None:
        """Создание записи abs_active"""

        user_login: str = self.login
        abs_id: Union[UUID, int, None] = self.dlg.abs_id
        position: int = int(self.dlg.content.controls[0].value)
        price_limitation: float = float(self.dlg.content.controls[1].value)
        response = requests.get(
            RequstsApi.CreactAbsActive.value
            + f"?user_login={user_login}&abs_id={abs_id}&position={position}&price_limitation={price_limitation}&start_time={self.time_start}&end_time={self.time_end}"
        )
        self.update_data(1, 3)
        if response.status_code == 200:
            self.dlg.open = False
            self.page.update()
        else:
            detail = response.json().get("detail")
            self.dlg.open = False
            self.page.update()

    def close_active(self, e, abs_id) -> None:
        """Закрытие записи abs_active"""

        requests.get(RequstsApi.StopAbsActive.value + f"?abs_active_id={abs_id}")
        self.dlg.open = False
        self.page.update()
        sleep(1)
        self.update_data(1, 2)
        self.update_data(1, 3)
