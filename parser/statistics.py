from typing import Dict, Tuple, List

import pandas as pd

from .constants import category_column, subcategory_column
from .currency_converter import CurrencyBucket
from .read_csv import read_csv, process_transaction_types

monthly_type = Dict[Tuple[int, int], CurrencyBucket]
subcategory_type = Dict[str, monthly_type]
data_type = Dict[str, subcategory_type]


def get_monthly_sum(group):
    current_category = {}
    for month, month_group in group.groupby(
            ["year", "month"], sort=False
    ):
        currency_total = CurrencyBucket()
        for currency, curr_group in month_group.groupby(
                "Currency", sort=False
        ):
            currency_total[currency] = curr_group["Amount"].sum()
        current_category[month] = currency_total
    return current_category


def get_monthly_expenses_by_category(df: pd.DataFrame) -> subcategory_type:
    categories = {}
    for category, group in df.groupby(category_column, sort=False):
        current_category = get_monthly_sum(group)
        categories[category] = current_category
    return categories


def get_monthly_expenses_by_subcategory(df: pd.DataFrame) -> data_type:
    categories = {}
    for category, group in df.groupby(category_column, sort=False):
        current_category = {}
        group = group.fillna(value=category)
        for subcategory, sub_group in group.groupby(
                subcategory_column, sort=False
        ):
            current_subcategory = get_monthly_sum(sub_group)
            current_category[subcategory] = current_subcategory
        categories[category] = current_category
    return categories


class CSVParser:
    def __init__(self, file_path: str = "data/all_transactions_2021.csv"):
        df = read_csv(file_path)
        transactions, misses = process_transaction_types(df)
        self.misses = misses
        self.expenses = transactions['Expense']
        self.incomes = transactions['Income']
        self.transfers = transactions['Money Transfer']
        self.subcategory_monthly = get_monthly_expenses_by_subcategory(
            self.expenses)
        self.category_monthly = get_monthly_expenses_by_category(self.expenses)

    def get_categories(self) -> List[str]:
        return list(self.category_monthly.keys())

    def get_category_subcategories(self, category: str) -> List[str]:
        return list(self.subcategory_monthly[category].keys())

    def get_category_history_in_currency(self, currency: str, category: str):
        history = self.category_monthly[category]
        return self._summarize(currency, history)

    @staticmethod
    def _summarize(currency: str, history: monthly_type):
        history_summary = {}
        for year_month, bucket in history.items():
            history_summary[year_month] = bucket.to_currency(currency)
        return history_summary

    def get_subcategory_history_in_currency(
            self, currency: str, category: str,
            sub_category: str
    ) -> Dict[Tuple[int, int], float]:
        history = self.subcategory_monthly[category][sub_category]
        return self._summarize(currency, history)
