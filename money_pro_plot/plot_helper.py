from typing import List, Tuple, Any

from matplotlib import pyplot as plt

from parser.statistics import CSVParser


def get_plot_figure_category(data: CSVParser, category):
    category_data = data.get_category_history_in_currency("AMD", category)
    dates = list(category_data.keys())
    amounts = list(category_data.values())

    return plot(dates, amounts)


def plot(x, y):
    filled_dates, filled_amounts = fill_in_empty_dates(x, y)
    plt_dates = ["{}/{}".format(i[1], i[0]) for i in filled_dates]
    fig = plt.figure(figsize=(18, 9))
    plt.plot(plt_dates, filled_amounts)
    plt.grid()
    plt.xticks(rotation=60)
    return fig


def get_plot_figure(data: CSVParser, category, subcategory):
    subcategory_data = data.get_subcategory_history_in_currency(
        "AMD", category, subcategory,
    )
    dates = list(subcategory_data.keys())
    amounts = list(subcategory_data.values())
    return plot(dates, amounts)


def fill_in_empty_dates(dates: List[Tuple[int, int]], amounts: List[Any]):
    # TODO fix me idiot
    years = [i[0] for i in dates]
    min_year = min(years)
    max_year = max(years)
    filled_dates = []
    filled_amounts = []
    for year in range(min_year, max_year + 1):
        for month in range(1, 13):
            if (year, month) in dates:
                filled_amounts.append(amounts[dates.index((year, month))])
            else:
                filled_amounts.append(0)
            filled_dates.append((year, month))

    return filled_dates, filled_amounts
