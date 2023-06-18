from matplotlib import pyplot as plt

from parser.statistics import CSVParser


def get_plot_figure(data: CSVParser, category, subcategory):
    subcategory_data = data.get_subcategory_history_in_currency(
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
