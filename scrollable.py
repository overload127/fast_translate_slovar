import tkinter as tk
import simpletable


class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(
            0, 0, window=self, anchor=tk.NW)

    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width=canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))


if __name__ == "__main__":
    """
    Как это работает и использовать
    """
    def getText():
        table.add_line_end(("lalala", "lololo"))
        scrollable_body.update()

    root = tk.Tk()

    header = tk.Frame(root)
    body = tk.Frame(root)
    footer = tk.Frame(root)
    header.pack(side=tk.TOP, expand=tk.NO, fill=tk.X)
    body.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
    footer.pack(side=tk.TOP, expand=tk.NO, fill=tk.X)

    tk.Label(header, text="The header").pack(
        side=tk.TOP, expand=tk.YES, fill=tk.X)
    tk.Button(header, text="Загрузить файл", command=getText).pack(
        side=tk.TOP, expand=tk.YES, fill=tk.X)
    tk.Label(footer, text="The Footer").pack(
        side=tk.LEFT, expand=tk.YES, fill=tk.X)

    scrollable_body = Scrollable(body, width=32)

    table = simpletable.SimpleTable(
        scrollable_body, ["Original value", "Translate value"], 0)
    table.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)

    scrollable_body.update()

    root.mainloop()
