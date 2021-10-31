from pynput.keyboard import Key, Controller
import keyboard
import threading
import time
import pyperclip
from infi.systray import SysTrayIcon
import pymsgbox
import os
import signal

# Сочитания клавишь
FOR_STRING = str()
FOR_WORD = str()
CAPS = str()
# Списки для перевода
LENG1 = str()
LENG2 = str()


def load_config():
    try:
        global FOR_STRING, FOR_WORD, CAPS, LENG1, LENG2

        with open("trn_config.config", encoding="UTF-8") as file:
            st = file.read().split("\n")

        for i in st:
            if not i or i[0] == "/":
                continue
            com = i.split(" = ", 1)
            if com[0] == "FOR_STRING":
                FOR_STRING = com[1].replace(", ", "+")
            elif com[0] == "FOR_WORD":
                FOR_WORD = com[1].replace(", ", "+")
            elif com[0] == "CAPS":
                CAPS = com[1].replace(", ", "+")
            elif com[0] == "LENG1":
                LENG1 = com[1].replace(", ", "+")
            elif com[0] == "LENG2":
                LENG2 = com[1].replace(", ", "+")

        return True

    except Exception as e:
        pymsgbox.alert(text=str(e), title="Error: config don't load", button="OK")
        print(e)
        return False


def convert(s):
    # Замена буквы на соответствующую из другого списка
    t = 0
    leng = 0
    rs = ""

    # Поиск первого символа, определяющего язык
    while t < len(s):
        if s[t] in LENG1 and s[t] in LENG2:
            t += 1
        elif s[t] in LENG1:
            leng = 1
            break
        elif s[t] in LENG2:
            leng = 2
            break
        else:
            t += 1

    if leng == 0:
        return s
    
    # Перевод с учётом языка прошлого символа
    for i in s:
        if i in LENG1 and i in LENG2:
            if leng == 1:
                rs += LENG2[LENG1.index(i)]
            else:
                rs += LENG1[LENG2.index(i)]

        elif not (i in LENG1 or i in LENG2):
            rs += i

        else:
            if i in LENG1:
                rs += LENG2[LENG1.index(i)]
                leng = 1
            else:
                rs += LENG1[LENG2.index(i)]
                leng = 2

    return rs


def for_string():

    kb = Controller()

    while True:
        try:

            keyboard.wait(FOR_STRING)

            time.sleep(0.5)

            with kb.pressed(Key.shift_l):
                with kb.pressed(Key.home):
                    time.sleep(0.1)

            with kb.pressed(Key.ctrl_l):
                with kb.pressed("c"):
                    time.sleep(0.1)

            s = pyperclip.paste()

            rs = convert(s)

            # Печать результата
            keyboard.write(rs)
            print(rs)

        except Exception as e:
            print(e)


def ex():
    os.kill(os.getpid(), signal.SIGTERM)    # Останавливает программу, убирая процесс. По-другому потоки не закрыть


if __name__ == '__main__':

    if not load_config():
        exit()  # Завершение работы, если настройки не загруженны

    # Создание потоков для каждой комбинации
    sr = threading.Thread(target=for_string)

    # Запуск потоков
    sr.start()

    # Добавление иконки в Tray
    menu_options = (("Update", None, lambda x: load_config()),)
    systray = SysTrayIcon("a-f.ico", "а-F Translator", menu_options, on_quit=lambda x: ex())
    systray.start()
