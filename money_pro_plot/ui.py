from tkinter import filedialog as fd
from tkinter import Tk, Button
from typing import Optional
from matplotlib import pyplot as plt

from parser.statistics import CSVParser


class MoneyProVisualiser:
    def __init__(self):
        self.main = Tk()
        self.file_select_button = Button(
            master=self.main, width=30,
            command=self.get_csv_file_content,
            text="Select MoneyPro export file to begin..."
        )
        self.file_select_button.pack()
        self.data: Optional[CSVParser] = None
        self.category_window = None
        self.subcategory_window = None
        self.category_buttons = []
        self.subcategory_buttons = []

        self.main.mainloop()

    def show_subcategory(self, category, subcategory: str):
        print("%s - %s" % (category, subcategory))

        subcategory_data = self.data.get_subcategory_history_in_currency(
            "AMD", category, subcategory,
        )
        dates = list(subcategory_data.keys())
        amounts = list(subcategory_data.values())
        dates = ["{}/{}".format(i[1], i[0]) for i in dates]
        plt.plot(dates, amounts)
        plt.show()

    def show_category(self, category: str):
        def subcategory_shower(c: str):
            def inner():
                return self.show_subcategory(category, c)

            return inner

        if self.subcategory_window:
            try:
                self.subcategory_window.destroy()
            except Exception as e:
                print("Cant destroy: %s" % e)

        self.subcategory_window = Tk()
        for subcategory in self.data.get_category_subcategories(category):
            button = Button(
                master=self.subcategory_window,
                text=subcategory, width=30,
                command=subcategory_shower(subcategory)
            )
            self.subcategory_buttons.append(button)
        [i.pack() for i in self.subcategory_buttons]

    def show_category_buttons(self):
        def category_shower(c: str):
            def inner():
                return self.show_category(c)

            return inner

        if self.category_window:
            try:
                self.category_window.destroy()
            except Exception as e:
                print("Cant destroy: %s" % e)
        self.category_window = Tk()

        for category in self.data.get_categories():
            button = Button(
                master=self.category_window,
                text=category, width=30,
                command=category_shower(category)
            )
            self.category_buttons.append(button)
        [i.pack() for i in self.category_buttons]

    def get_csv_file_content(self):
        file = fd.askopenfile(mode="r")
        print("File selected")
        self.data = CSVParser(file)
        print("Data read: %s" % self.data)
        self.file_select_button.destroy()
        self.show_category_buttons()


g = MoneyProVisualiser()
