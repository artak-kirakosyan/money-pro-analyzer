import tkinter
from tkinter import Tk, Button
from tkinter import filedialog as fd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from money_pro_plot.plot_helper import get_plot_figure, get_plot_figure_category
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
        self.main = Tk(className=" MoneyPro Visualizer ")
        self.data = None
        self.show_file_selector()
        self.main.mainloop()

    def clean(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def show_file_selector(self):
        self.clean()
        file_selector_frame = tkinter.Frame(self.main)
        tkinter.BooleanVar(file_selector_frame)
        tkinter.Label(
            file_selector_frame, text="Select Money Pro export CSV file to begin",
            font=get_font(TITLE_SIZE, is_bold=True)
        ).grid(row=0)
        file_select_button = Button(
            master=self.main, width=BUTTON_WIDTH,
            command=self.get_csv_file_selector,
            text="Choose the file", font=get_font()
        )
        file_select_button.grid(row=1)

    def get_csv_file_selector(self):
        file = fd.askopenfile(mode="r")
        self.data = CSVParser(file)
        self.show_category_buttons()

    def show_category_subcategories(self, category: str):
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

        def subcategory_shower(c: str):
            def inner():
                return self.show_subcategory_plot(category, c)

            return inner
        index = 2
        for index, subcategory in enumerate(self.data.get_category_subcategories(category), start=2):
            button = Button(
                master=subcategory_window,
                text=subcategory, width=BUTTON_WIDTH, font=get_font(),
                command=subcategory_shower(subcategory)
            )
            button.grid(row=index)
        b = Button(
            master=subcategory_window,
            text="Show category summary", width=BUTTON_WIDTH, font=get_font(TITLE_SIZE, is_bold=True),
            command=self.show_category_plot_action(category)
        )
        b.grid(row=index)

    def category_subcategories_shower(self, category: str):
        def inner():
            return self.show_category_subcategories(category)

        return inner

    def show_category_buttons(self):
        self.clean()
        category_window = tkinter.Frame(self.main)
        category_window.grid()
        tkinter.Label(
            category_window, text="Select category", font=get_font(TITLE_SIZE, is_bold=True)
        ).grid(row=0)
        button = Button(
            master=category_window,
            text="Back to file selector", width=BUTTON_WIDTH, font=get_font(TITLE_SIZE, is_bold=True),
            command=self.show_file_selector
        )
        button.grid(row=1)
        for index, category in enumerate(self.data.get_categories(), start=2):
            button = Button(
                master=category_window,
                text=category, width=BUTTON_WIDTH, font=get_font(),
                command=self.category_subcategories_shower(category)
            )
            button.grid(row=index)

    def show_category_plot_action(self, category: str):
        def inner():
            return self.show_category_plot(category)

        return inner

    def show_category_plot(self, category: str):
        fig = get_plot_figure_category(self.data, category)

        def back_to_sub_categories():
            return self.show_category_subcategories(category)

        self.plot_figure(fig, category, back_to_sub_categories)

    def plot_figure(self, fig: Figure, title: str, fallback):

        self.clean()
        plot_window = tkinter.Frame(self.main)
        plot_window.grid()
        tkinter.Label(
            plot_window, text=title,
            font=get_font(TITLE_SIZE, is_bold=True)
        ).grid(row=0)

        b = Button(
            master=plot_window,
            text="Back to sub-categories", width=BUTTON_WIDTH, font=get_font(TITLE_SIZE, is_bold=True),
            command=fallback
        )
        b.grid(row=1)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, plot_window, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=2)
        canvas.get_tk_widget().grid(row=3)

    def show_subcategory_plot(self, category, subcategory: str):
        fig = get_plot_figure(self.data, category, subcategory)

        def back_to_sub_categories():
            return self.show_category_subcategories(category)

        self.plot_figure(fig, category + " / " + subcategory, back_to_sub_categories)
