import keyboard
import threading
import pyautogui
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


def convert(x):
    # Замена буквы на соответствующую из другого списка
    if x in LENG1:
        return LENG2[LENG1.index(x)]
    if x in LENG2:
        return LENG1[LENG2.index(x)]
    return x


def for_string():
    while True:
        try:

            rs = ""  # Результат

            keyboard.wait(FOR_STRING)   # Ожидание нажатия комбинации клавишь
            time.sleep(0.3)
            pyautogui.hotkey("shift", "home")   # Комбинация клавишь, выделающая всю строку
            time.sleep(0.01)
            pyautogui.hotkey("alt", "shift")    # Смена языка
            time.sleep(0.01)
            pyautogui.hotkey("ctrl", "c")   # Копирование текста строки
            time.sleep(0.01)

            s = pyperclip.paste()

            if type(s) != str:
                pyautogui.hotkey("ctrl", "z")   # Если комбинация применена не к тексту, выделение уберается
                return

            for i in s:
                if i == "\n":
                    break
                rs += convert(i)

            # Печать результата
            print(rs)
            keyboard.write(rs)

        except Exception as e:
            print(e)


def for_word():
    while True:
        try:
            rs = ""

            keyboard.wait(FOR_WORD)
            time.sleep(0.3)
            pyautogui.hotkey("shift", "ctrl", "left")   # Комбинация для выделения последнего слова
            time.sleep(0.01)
            pyautogui.hotkey("alt", "shift")
            time.sleep(0.01)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.01)

            s = pyperclip.paste()

            if type(s) != str:
                pyautogui.hotkey("ctrl", "z")
                return

            for i in s:
                if i == "\n":
                    break
                rs += convert(i)

            print(rs)
            keyboard.write(rs)
        except Exception as e:
            print(e)


def for_caps():
    while True:
        try:
            rs = ""

            keyboard.wait(CAPS)
            time.sleep(0.3)
            pyautogui.hotkey("shift", "home")
            time.sleep(0.01)
            pyautogui.hotkey("alt", "shift")
            time.sleep(0.01)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.01)

            s = pyperclip.paste()

            if type(s) != str:
                pyautogui.hotkey("ctrl", "z")
                return

            # Изменение регистра буквы на обратный
            for i in s:
                if i.islower():
                    rs += i.upper()
                else:
                    rs += i.lower()

            print(rs)
            keyboard.write(rs)
        except Exception as e:
            print(e)


def ex():
    os.kill(os.getpid(), signal.SIGTERM)    # Останавливает программу, убирая процесс. По другому потоки не закрыть


if __name__ == '__main__':

    if not load_config():
        exit()  # Завершение работы, если настройки не загруженны

    # Создание потоков для каждой комбинации
    sr = threading.Thread(target=for_string)
    wo = threading.Thread(target=for_word)
    ca = threading.Thread(target=for_caps)

    # Запуск потоков
    sr.start()
    wo.start()
    ca.start()

    # Добавление иконки в Tray
    menu_options = (("Update", None, lambda x: load_config()),)
    systray = SysTrayIcon("a-f.ico", "а-F Translator", menu_options, on_quit=lambda x: ex())
    systray.start()
