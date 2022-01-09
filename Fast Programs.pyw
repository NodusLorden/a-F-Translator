from infi.systray import SysTrayIcon
import os
from PIL import Image
import extract_icon


def load_programs():
    try:
        with open("Programs.txt", encoding="UTF-8") as f:
            programs = list(filter(lambda x: x, f.read().split("\n")))
    except Exception as er:
        return er
    return programs


class PrButtons:

    def __init__(self, path: str):
        self._path = path.strip("'").strip('"')
        self._name = self._getfilename(self._path).rstrip(".lnk").rstrip(".exe")
        self._imgpath = "IconCash/" + self._name + ".png"
        self._iocnpath = "IconCash/" + self._name + ".ico"
        try:
            icon = extract_icon.ExtractIcon(self._path).get_icon(0)

            with open(self._imgpath, mode="wb") as f:
                f.write(icon)

            img = Image.open(self._imgpath)
            img.save(self._iocnpath, format='ICO')

        except Exception as er:
            print(er)
            self._iconpath = None

    def get_option(self):
        return self._name, self._iocnpath, self.__call__

    def __call__(self, *args, **kwargs):
        try:
            os.startfile(self._path)
        except Exception as er:
            print(er)

    @staticmethod
    def _getfilename(path):
        for i in range(len(path) - 1, -1, -1):

            if path[i] == "\\" or path[i] == "/":
                return path[i + 1:]


def main():

    menu_options = []

    for path in load_programs():
        prog = PrButtons(path)
        menu_options.append(prog.get_option())
        print(prog.get_option())

    systray = SysTrayIcon("icon.ico", "Programs", tuple(menu_options), on_quit=exit)
    systray.start()


if __name__ == '__main__':
    main()
