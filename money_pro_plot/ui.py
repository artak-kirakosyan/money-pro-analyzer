import tkinter
from tkinter import Tk, Button
from tkinter import filedialog as fd
from typing import Optional

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from parser.statistics import CSVParser

BUTTON_WIDTH = 50
SIZE = 12
TITLE_SIZE = 16


def get_font(size: int = SIZE, is_bold: bool = False):
    font = ['Times', size]
    if is_bold:
        font.append("bold")
    return font


class MoneyProVisualiser:
    def __init__(self):
        self.main = Tk(className=" MoneyPro Visualizer")
        file_select_button = Button(
            master=self.main, width=BUTTON_WIDTH,
            command=self.get_csv_file_content,
            text="Select MoneyPro export file to begin...", font=get_font()
        )
        file_select_button.pack()
        self.data: Optional[CSVParser] = None

        self.main.mainloop()

    def show_category(self, category: str):
        def subcategory_shower(c: str):
            def inner():
                return self.show_subcategory(category, c)

            return inner

        self.clean()
        subcategory_window = tkinter.Frame(self.main)
        subcategory_window.grid()
        tkinter.Label(
            subcategory_window, text="Select sub category",
            font=get_font(TITLE_SIZE, is_bold=True)
        ).grid(row=0)
        b = Button(
            master=subcategory_window,
            text="Back to categories", width=BUTTON_WIDTH, font=get_font(TITLE_SIZE, is_bold=True),
            command=self.show_category_buttons
        )
        b.grid(row=1)
        subcategory_buttons = []
        for index, subcategory in enumerate(self.data.get_category_subcategories(category), start=2):
            button = Button(
                master=subcategory_window,
                text=subcategory, width=BUTTON_WIDTH, font=get_font(),
                command=subcategory_shower(subcategory)
            )
            button.grid(row=index)
            subcategory_buttons.append(button)

    def show_category_buttons(self):
        def category_shower(c: str):
            def inner():
                return self.show_category(c)

            return inner

        self.clean()
        category_window = tkinter.Frame(self.main)
        category_window.grid()
        tkinter.Label(category_window, text="Select category", font=get_font(TITLE_SIZE, is_bold=True)).grid(row=0)
        category_buttons = []
        for index, category in enumerate(self.data.get_categories(), start=1):
            button = Button(
                master=category_window,
                text=category, width=BUTTON_WIDTH,
                command=category_shower(category)
            )
            button.grid(row=index)
            category_buttons.append(button)

    def get_csv_file_content(self):
        file = fd.askopenfile(mode="r")
        self.data = CSVParser(file)
        self.show_category_buttons()

    def clean(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def show_subcategory(self, category, subcategory: str):
        fig = self.get_plot_figure(category, subcategory)

        self.clean()
        plot_window = tkinter.Frame(self.main)
        plot_window.grid()
        tkinter.Label(
            plot_window, text=category + " / " + subcategory,
            font=get_font(TITLE_SIZE, is_bold=True)
        ).grid(row=0)

        def back_to_sub_categories():
            return self.show_category(category)

        b = Button(
            master=plot_window,
            text="Back to sub-categories", width=BUTTON_WIDTH, font=get_font(TITLE_SIZE, is_bold=True),
            command=back_to_sub_categories
        )
        b.grid(row=2)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()

        canvas.get_tk_widget().grid(row=3)

    def get_plot_figure(self, category, subcategory):
        subcategory_data = self.data.get_subcategory_history_in_currency(
            "AMD", category, subcategory,
        )
        dates = list(subcategory_data.keys())
        amounts = list(subcategory_data.values())
        dates = ["{}/{}".format(i[1], i[0]) for i in dates]
        fig = plt.figure(figsize=(15, 9))
        plt.plot(dates, amounts)
        plt.grid()
        plt.xticks(rotation=60)
        return fig


g = MoneyProVisualiser()
