#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
HEADER = 0
BODY = 1
COLUMN1 = 0
COLUMN2 = 1
COLUMN3 = 2
CHECKVAR = 1
WIDGET = 0


class SimpleTable(tk.Frame):
    def __init__(self, parent, names, rows=10):
        # use black background so it "peeks through" to
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = [[], []]
        self.vars = [[], []]
        self.__END = 0
        # hrader
        self.add_header(names)
        # body
        for row in range(1, rows+1):
            self.__add_line_end(row)

        # self.scrolltable = tk.Scrollbar(self, command=table.yview)
        # scrolltable.pack(side=tk.RIGHT, fill=tk.Y)

        for column in range(3):
            if column == 2:
                self.grid_columnconfigure(column, weight=0)
            else:
                self.grid_columnconfigure(column, weight=1)
        
        # Добавляем события копирования прирусской раскладке
        self.event_add('<<Paste>>', '<Control-igrave>')
        self.event_add("<<Copy>>", "<Control-ntilde>")

    def set_in_body(self, row, column, value):
        var = self.vars[BODY][row][column]
        var.set(value)

    def add_header(self, names):
        current_row_widgets = []
        current_row_values = []
        entry_var = tk.StringVar()
        entry_widget = tk.Entry(
            self, text=entry_var, borderwidth=0,
            width=30, justify=tk.CENTER, state='readonly')
        entry_widget.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        entry_var.set(names[0])
        current_row_widgets.append(entry_widget)
        current_row_values.append(entry_var)
        entry_var = tk.StringVar()
        entry_widget = tk.Entry(
            self, text=entry_var, borderwidth=0, width=30,
            justify=tk.CENTER, state='readonly')
        entry_widget.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
        entry_var.set(names[1])
        current_row_widgets.append(entry_widget)
        current_row_values.append(entry_var)
        check_var = tk.BooleanVar()
        check_button_widget = tk.Checkbutton(
            self, text="", variable=check_var, onvalue=1, offvalue=0,
            command=self.get_obr_header())
        check_button_widget.grid(row=0, column=2, sticky="e", padx=1,
                                 pady=1)
        current_row_widgets.append(check_button_widget)
        current_row_values.append(check_var)
        self._widgets[HEADER].append(current_row_widgets)
        self.vars[HEADER].append(current_row_values)

    def add_line_end(self, values):
        self.__END += 1
        self.__add_line_end(self.__END, values)

    def __add_line_end(self, row, values=None):
        current_row_widgets = []
        current_row_values = []
        entry_var = tk.StringVar()
        entry_widget = tk.Entry(
            self, text=entry_var, borderwidth=0,
            width=30, justify=tk.RIGHT, state='readonly')
        entry_widget.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
        if values:
            entry_var.set(values[0])
        else:
            entry_var.set("%s/%s" % (row-1, 0))
        current_row_widgets.append(entry_widget)
        current_row_values.append(entry_var)
        entry_var = tk.StringVar()
        entry_widget = tk.Entry(
            self, text=entry_var, borderwidth=0, width=30)
        entry_widget.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
        if values:
            entry_var.set(values[1])
        else:
            entry_var.set("%s/%s" % (row-1, 1))
        current_row_widgets.append(entry_widget)
        current_row_values.append(entry_var)
        check_var = tk.BooleanVar()
        check_button_widget = tk.Checkbutton(
            self, text="", variable=check_var, onvalue=1, offvalue=0,
            command=self.get_obr_body(row-1))
        check_button_widget.grid(row=row, column=2, sticky="e", padx=1,
                                 pady=1)
        current_row_widgets.append(check_button_widget)
        current_row_values.append(check_var)
        self._widgets[BODY].append(current_row_widgets)
        self.vars[BODY].append(current_row_values)

    def get_obr_body(self, row):
        """
        Это замыкание.
        Оно создаёт для каждого чекбокса (в body таблици) свою функцию,
        которую связывает по указанной строке при инициализации
        """
        def eventcheck():
            widget = self._widgets[BODY][row][COLUMN2]
            var = self.vars[BODY][row][COLUMN3]
            if var.get():
                widget.config(state='readonly')
            else:
                widget.config(state='normal')
        return eventcheck

    def get_obr_header(self):
        """
        Это замыкание.
        Оно создаёт функцию для чекбокса в header
        """
        def eventcheck():
            """
            Выполняет переключение всех чекбоксов в body таблицы
            Выполняет переключение доступности поля в колонке 2
            """
            var_head = self.vars[HEADER][0][COLUMN3]
            value_head = var_head.get()
            for i in range(len(self._widgets[BODY])):
                var_line = self.vars[BODY][i][COLUMN3]
                if value_head != var_line.get():
                    widget_check = self._widgets[BODY][i][COLUMN3]
                    widget_input = self._widgets[BODY][i][COLUMN2]
                    if value_head == 0:
                        widget_check.deselect()
                        widget_input.config(state='normal')
                    else:
                        widget_check.select()
                        widget_input.config(state='readonly')

        return eventcheck

    @property
    def END(self):
        return self.__END


if __name__ == "__main__":
    class ExampleApp(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            self.table = SimpleTable(
                self, ["Original value", "Translate value"], 10)
            self.table.pack(side="top", fill="x")
            self.table.set_in_body(6, 1, "1111")

    app = ExampleApp()
    app.mainloop()
