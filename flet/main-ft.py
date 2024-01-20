import random
import flet as ft
from threading import Thread
import qrcode
import requests
import serial
from time import time
from json import loads

import math

card_id = None

rows_of_buys = 4
rows_of_olimps = 4

def check_user(card_id):
    url = 'https://whoid.ru/card/api/check'

    params = dict(
        card=card_id
    )

    resp = requests.get(url=url, params=params)
    print(resp.text)
    return loads(resp.text)

def build_reg_screen(card_id):
    url = f"https://whoid.ru/card/reg?card={"_".join(card_id.split(' '))}"
    c = ft.Column([
        ft.Text("Ой-Ой. Вы не зарегестрированы(", text_align=ft.TextAlign.CENTER, size=35),
        ft.Image(
        src=f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={url}",
        width=400,
        height=400,
        fit=ft.ImageFit.CONTAIN),
        ft.Text("Держи qr для регестриции)", text_align=ft.TextAlign.CENTER, size=30)
    ])
    return c

def card():
    global card_id
    print("Система заряботяля")
    ser = serial.Serial('/dev/tty.usbserial-1410', 9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            if ser.readline().decode('utf-8').rstrip() == "Found RFID/NFC reader":
                print("Connect sucsed")
                break
    while True:
        if ser.in_waiting > 0:
            smth = ser.readline().decode('utf-8').rstrip()[7:]
            if not smth == "":
                card_id = {"card_id": smth, "time": time()}
                print(card_id)


def create_qrcode(text):
    with open('qr.png', 'w') as file:
        file = qrcode.make(text)
        file.save('./qr.png')


def build_main(items, predmets):
    create_qrcode('whoid.ru')

    up_part = ft.Row(
        [
            ft.Text(
                "Вася Пупкин",
                size=20,
            ),
            ft.Container(
                content=ft.Row([
                    ft.Text(
                        "2800 КК",
                        size=20,
                    ),
                    ft.Image(
                        src="static/stone.png",
                        width=100,
                        height=100,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=ft.border_radius.all(5),
                    )], spacing=40, alignment=ft.MainAxisAlignment.END),
                alignment=ft.alignment.top_right,
                width=50,
                height=50,
            )], spacing=40, alignment=ft.MainAxisAlignment.CENTER)

    c = []
    itir = math.ceil(len(items) / rows_of_buys)
    for i in range(rows_of_buys):
        r = []
        for j in range(itir):
            try:
                r.append(ft.Text(
                    f"{items[i * itir + j]} - {random.randint(100, 1000)}KK - {random.choice(['Сгорело на складе', 'Ожидает получения', 'Доставлено'])}",
                    size=15))
            except BaseException as e:
                pass
        c.append(ft.Row(r, spacing=55))
    shops = ft.Column(c, spacing=10)
    buyes = ft.Row([
        ft.Column([
            ft.Row([ft.Text(
                "Ваши покупки:",
                size=30, text_align=ft.TextAlign.CENTER, italic=True
            )], alignment=ft.MainAxisAlignment.CENTER),
            shops
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER)

    c = []
    itir = math.ceil(len(predmets) / rows_of_olimps)
    for i in range(rows_of_olimps):
        r = []
        for j in range(itir):
            try:
                r.append(ft.Text(
                    f"{predmets[i * itir + j]} - {random.randint(100, 1000)}KK - 12.01.2077",
                    size=15))
            except BaseException as e:
                pass
        c.append(ft.Row(r, spacing=55))
    olimp = ft.Column(c, spacing=10)
    olipmps = ft.Row([
        ft.Column([
            ft.Row([ft.Text(
                "Олимпиады доступные для участия:",
                size=30, text_align=ft.TextAlign.CENTER, italic=True
            )], alignment=ft.MainAxisAlignment.CENTER),
            olimp
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER)

    # ft.Image(
    # src=f"https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=whoid.ru",
    # width=100,
    # height=100,
    # fit=ft.ImageFit.CONTAIN,

    name_pr = ft.Row([ft.Text(
        "Активный школьник",
        size=30,
        weight=ft.FontWeight.W_900,
        selectable=True
    )], alignment=ft.MainAxisAlignment.CENTER)

    fn_r = ft.Column([name_pr, up_part, ft.Divider(
        height=9,
        thickness=3
    ), buyes, ft.Divider(
        height=9,
        thickness=3
    ), olipmps])
    return fn_r


def screen_saver_build():
    screen_saver = ft.Text("Приложите карточку", text_align=ft.TextAlign.CENTER)
    return screen_saver


def main(page: ft.Page):
    page.title = "Активный школьник"
    # page.scroll = "adaptive"

    screensaver = screen_saver_build()

    c = ft.AnimatedSwitcher(
        screensaver,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=500,
        switch_in_curve=ft.AnimationCurve.EASE_IN,
        switch_out_curve=ft.AnimationCurve.EASE_OUT,
    )
    page.add(c)

    def animate(content):
        c.content = content
        c.update()
        page.update()

    items = [
        'Ручка', 'Блокнот', 'Футболка', 'Интульгенция', 'Кружка', 'Мышка',
    ]
    predmets = [
        'Математика', "Физика", "Русский язык", "Биология", "Информатика", "Химия", "История"
    ]
    prev = None
    change = False
    usr = False
    while True:
        if prev != card_id:
            try:
                usr = check_user(card_id["card_id"])["error"]
                usr = True
            except Exception as e:
                usr = False
            print(usr)
            if not change:
                if not usr:
                    ma = build_main(items, predmets)
                    animate(ma)
                    change = True
                else:
                    animate(build_reg_screen(card_id["card_id"]))
                    change = True
            #print(time() - card_id["time"])
            if time() - card_id["time"] > 5:
                print("prev")
                prev = card_id
                animate(screensaver)
                change = False

    page.update()


Thread(target=card).start()

ft.app(target=main)
