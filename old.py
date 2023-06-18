import math
from collections import defaultdict
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib

import pandas as pd

from parser.read_csv import read_csv


def get_expenses(file_path) -> pd.DataFrame:
    df = read_csv(file_path)
    exps = df[df['Transaction Type'] == "Expense"].copy()
    exps.drop(["Amount received", "Account (to)", "Balance", "Transaction Type", "Agent"], axis=1, inplace=True, errors='ignore')
    return exps


def main():
    expenses = get_expenses("data/all_transactions.csv")
    expenses['YearMonth'] = expenses['Date'].apply(lambda x: x.strftime("%y/%m"))

    expenses = expenses[
        (expenses['Date'] > datetime(year=2020, month=8, day=1))
        # (expenses['Date'] < datetime(year=2021, month=7, day=1))
    ]
    expenses['Final Category'] = expenses['Category'].apply(lambda x: x.split(":")[-1].strip())
    expenses['First Category'] = expenses['Category'].apply(lambda x: x.split(":")[0].strip())
    per_month = expenses.groupby("YearMonth")
    q = {}
    for group, group_vals in per_month:
        expenses_per_month: pd.Series = group_vals.groupby("First Category")["Amount"].sum()
        expenses_per_month.sort_values(ascending=False, inplace=True)
        q[group] = expenses_per_month.to_dict()

    all_categories = set()
    for values in q.values():
        for cat in values.keys():
            all_categories.add(cat)

    per_category = defaultdict(list)
    months = []
    for month, category_vals in q.items():
        for category in all_categories:
            per_category[category].append(
                category_vals.get(category, 0)
            )
        months.append(month)

    return per_category, months


categories, dates = main()

drop_list = [
    'Groceries Groceries',
    'Crypto',
    'Medical Groceries',
    "Utilities Canada"
]

for d in drop_list:
    categories.pop(d, None)

font = {'size': 7}

matplotlib.rc('font', **font)

vertical = 3
horiz = math.ceil(len(categories) / vertical)

fig, axes = plt.subplots(horiz, vertical)
count = 0
horiz_index = 0

for category, category_values in categories.items():

    axes[horiz_index, count].bar(dates, category_values)
    axes[horiz_index, count].set_title(category)
    count += 1
    if count >= vertical:
        count = 0
        horiz_index += 1

plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.3)
