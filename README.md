# а-F-Translator

## Версия 0.2.0

Программа для быстрого перевода текста, написанного не на нужном языке.

После запуска в в Taskbar появтится мелкая иконка. Если нажать по ней правой кнопкой мыши и выбрать Quit, программа закроется.

![Taskbar](https://user-images.githubusercontent.com/58140098/121680844-38d88400-cae4-11eb-8fbc-41bc5d6fa5af.png)

![Taskbar2](https://user-images.githubusercontent.com/58140098/121680863-41c95580-cae4-11eb-8c62-5038c7ce3654.png)

#### *Для работы программа использует буфер обмена, поэтому не храните ничего ценного во время применения команд.*

## Команды

Alt + Shift + A (Ф на русской раскладке) - заменияет текст в строке, в которой стоит курсор, на транслированный.

*Ctrl + Alt + A - заменяет последнее слово в строке на транслированное.* в текущей версии не доступна

*Alt + Caps Lock - меняет регистр всех букв в строке.* в текущей версии не доступна

## Настройка

В папке с программой есть файл *trn_config.config*, его можно открыть в блоконоте.

![image](https://user-images.githubusercontent.com/58140098/121682615-80600f80-cae6-11eb-844c-20c510e95d8c.png)

После *FOR_STRING, FOR_WORD, CAPS* через " = " нужно указать кнопки для использования функций. Если их несколько, нужно использовать разделитель ", ". Можно использовать кнопки с буквами, цифры, кнопки *F1, F2, F3...* и названия кнопок: *alt, shift, ctrl, win, menu, capslock, tab, backspace, enter, insert, delete, end, home, pageup, pagedown, num lock, right, left, up, down* (они проверены).

*LENG1 и LENG2* это список, по которому идёт замена. Каждая буква заменяется на букву из 2 списка, имеющую тот же номер от начала строки.

## Дополнительно

Файлы *а-F Translator.bat и launch.vbs* нужны для запуска программы через питон, при этом окна консоли не будет видно. Для батника можно сделать ярлык и кинуть а автозагрузку.
