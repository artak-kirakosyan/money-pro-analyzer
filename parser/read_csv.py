from typing import Dict, Tuple

import pandas as pd

from .constants import category_column, subcategory_column, \
    date_column, transaction_type_column


def get_currency(amount: str) -> str:
    return "".join([i for i in amount if i.isalpha()])


def remove_currency(amount: str) -> float:
    return float(
        "".join(
            [
                i for i in amount if not i.isalpha() and i not in "$,€"
            ]
        )
    )


currency_remove_columns = [
    "Amount", "Balance"
]


def read_csv(file_path) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=file_path,
        parse_dates=[date_column, ],
        sep=";",
    )
    df.drop(["Unnamed: 10", "Agent"], inplace=True, axis=1, errors="ignore")

    df['Currency'] = df['Amount'].apply(get_currency)
    df['Currency_Balance'] = df['Balance'].apply(get_currency)
    for col in currency_remove_columns:
        df[col] = df[col].apply(remove_currency)
    return df


def separate_subcategory(df: pd.DataFrame):
    category = df[category_column]
    # TODO multiple transactions in 1 row(2 colons in 1 category)
    df[subcategory_column] = category.apply(
        lambda x: None if len(x.split(": ")) == 1 else x.split(": ")[1])
    df[category_column] = category.apply(lambda x: x.split(": ")[0])
    return df


def separate_date_components(df: pd.DataFrame):
    df['year'] = df[date_column].apply(lambda x: x.year)
    df['month'] = df[date_column].apply(lambda x: x.month)
    df['day'] = df[date_column].apply(lambda x: x.day)
    df['hour'] = df[date_column].apply(lambda x: x.hour)
    df['minute'] = df[date_column].apply(lambda x: x.minute)

    return df


def process_expenses(df: pd.DataFrame) -> pd.DataFrame:
    df = separate_subcategory(df)
    df = separate_date_components(df)
    df = df.drop(["Amount received", "Account (to)",
                  transaction_type_column], axis=1)
    return df.reset_index(drop=True)


def process_incomes(df: pd.DataFrame) -> pd.DataFrame:
    df = separate_subcategory(df)
    df = separate_date_components(df)
    df = df.drop(["Amount received", "Account (to)",
                  transaction_type_column], axis=1)
    return df.reset_index(drop=True)


def process_transfers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop([transaction_type_column, category_column], axis=1)
    return df.reset_index(drop=True)


transaction_type_processors = {
    "Expense": process_expenses,
    "Income": process_incomes,
    "Money Transfer": process_transfers,
}


def process_transaction_types(
        df: pd.DataFrame
) -> Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame]]:
    transactions = {}
    missing = {}
    for tr_type, group in df.groupby(transaction_type_column, sort=False):
        try:
            processor = transaction_type_processors[tr_type]
        except KeyError:
            print("Processor not found for %s, skipping" % tr_type)
            missing[tr_type] = group
            continue
        transactions[tr_type] = processor(group)
    return transactions, missing
