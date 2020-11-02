#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog as fd
import re
import simpletable as s_table
import scrollable as scroll_l
from googletrans import Translator


class Mywindow:
    def __init__(self, master):
        """
        Создаём окно со следующими элементами:
        кнопки - 5 штук
        таблица - 1 штука
        """
        # создаём контейнеры, для правильного размещения объектов
        self.frame_top = tk.LabelFrame(master, text="Buttons")
        self.frame_bot = tk.LabelFrame(master, text="Table")
        self.frame_top_1 = tk.Frame(self.frame_top)
        self.frame_top_2 = tk.Frame(self.frame_top)
        # Размещаем контейнеры на форме
        self.frame_top.pack(side=tk.TOP, expand=tk.NO, fill=tk.X)
        self.frame_bot.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.frame_top_1.pack(side=tk.TOP, expand=tk.NO, fill=tk.X)
        self.frame_top_2.pack(side=tk.TOP, expand=tk.NO, fill=tk.X)

        # Создаём кнопки
        self.button_load_file = tk.Button(
            self.frame_top_1, text="Load file (EN)", command=self.getText)
        self.button_to_buffer = tk.Button(
            self.frame_top_2, text="Load in buffer from original text",
            command=self.toBuffer)
        self.button_from_buffer = tk.Button(
            self.frame_top_2, text="Paste translate from buffer",
            command=self.fromBoffer)
        self.button_fast_translate = tk.Button(
            self.frame_top_1, text="Fast translate",
            command=self.fastTranslate)
        self.button_seve_file = tk.Button(
            self.frame_top_1, text="Save translate (.string)",
            command=self.saveFile)
        # Размещаем элементы (кнопки и поля) в соответствующих контейнерах
        self.button_load_file.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        self.button_to_buffer.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        self.button_from_buffer.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        self.button_fast_translate.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        self.button_seve_file.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

        # Создаём контейнер для таблицы
        self.scrollable_body = scroll_l.Scrollable(self.frame_bot, width=32)
        # Создаём таблицу внутри контейнера для таблицы
        self.table = s_table.SimpleTable(
            self.scrollable_body, ["Original text", "Translate text"], 0)
        self.table.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        self.scrollable_body.update()

        self.root = master
        self.variable = []

    def getText(self):
        """
        Открывает файл. Загружает его в память программы
        """
        file_name = fd.askopenfilename()
        if file_name:
            with open(file_name, "r") as file:
                all_text = file.read()

            self.create_clean_text(all_text)

    def create_clean_text(self, all_text):
        """
        Получает текст из файла и вытаскивает из него переменные
        и перевод на английском языке.
        Далее заполняет левую часть таблицы полученными словами
        """
        # '"(.+)": "(.+)"'
        if all_text:
            result = re.findall(r'"(.+)": "(.+)"', all_text)

            # Здесь можно было бы проверять на английский язык
            # lang = result[0][1]
            for i in range(1, len(result)):
                self.variable.append(result[i][0])
                original_text = result[i][1]
                transtate_text = ''
                self.table.add_line_end((original_text, transtate_text))

            self.scrollable_body.update()
            self.toBuffer()

    def toBuffer(self):
        """
        Загружает в буфер обмена слова из левой колонки таблицы.
        (Предполагается что там английские слова)
        """
        all_phrases = ''
        for i in range(self.table.END):
            all_phrases += self.table.vars[s_table.BODY][i][s_table.COLUMN1].get()+'\n'
        if all_phrases != '':
            self.root.clipboard_clear()
            self.root.clipboard_append(all_phrases)

    def fromBoffer(self):
        """
        Загружает слова из буфера обмена в правую колонку таблицы.
        (Предполагается что там русский текст)
        """
        text_from_buffer = self.root.clipboard_get().split('\n')
        if text_from_buffer:
            for i in range(self.table.END):
                self.table.vars[s_table.BODY][i][s_table.COLUMN2].set(
                    text_from_buffer[i])

    def completedText(self):
        """
        Собирает слова из правой колонки таблицы
        и объединяет в одну строку со всеми необходимыми мета-данными
        """
        all_phrases = []
        for i in range(self.table.END):
            all_phrases.append(
                self.table.vars[s_table.BODY][i][s_table.COLUMN2].get())

        all_phrases = []
        for i in range(self.table.END):
            line = self.table.vars[s_table.BODY][i][s_table.COLUMN2].get()
            if i == self.table.END - 1:
                line_text = f"    \"{self.variable[i]}\": \"{line}\"\n"
            else:
                line_text = f"    \"{self.variable[i]}\": \"{line}\",\n"
            all_phrases.append(line_text)

        out_text = ''.join(('{\n',
                            '  "LocaleUri": "base/ru.locale",\n',
                            '  "ItemsUri": null,\n',
                            '  "Items": {\n',
                            *all_phrases,
                            '  }\n',
                            '}'))

        return out_text

    def saveFile(self):
        """
        Сохраняет полученный текст в выбранный файл
        Проверяет наличие расширения в имени файла (.string)
        Добавляет соответствующее расширение, если не было найдено.
        """
        file_name = fd.asksaveasfilename(
            filetypes=(("Lang files", "*.strings"),
                       ("TXT files", "*.txt"),
                       ("All files", "*.*")))
        if file_name:
            if not file_name.endswith(".strings"):
                file_name = ''.join((file_name, ".strings"))
            text = self.completedText()
            with open(file_name, 'w',  encoding='utf8') as file:
                file.write(text)

    def fastTranslate(self):
        """
        Вытаскивает слова из левой колонки и отправляет в гугл переводчик
        Далее вставляет в правый столбец полученный перевод
        """
        translator = Translator()
        all_phrases = []
        for i in range(self.table.END):
            all_phrases.append(
                self.table.vars[s_table.BODY][i][s_table.COLUMN1].get())
        if all_phrases == []:
            return

        results = translator.translate(all_phrases, src='en', dest='ru')

        for i in range(self.table.END):
            self.table.vars[s_table.BODY][i][s_table.COLUMN2].set(
                results[i].text)


if __name__ == "__main__":
    root = tk.Tk()

    first_win = Mywindow(root)

    root.mainloop()
