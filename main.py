from parser.statistics import CSVParser

c = CSVParser("data/all_transactions_2021.csv")

res = c.get_subcategory_history_in_currency("AMD", "Utilities", "Cell Phone")
