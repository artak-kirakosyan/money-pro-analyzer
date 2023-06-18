from parser.statistics import CSVParser

c = CSVParser("data/transactions_2023_06_18.csv")

res = c.get_subcategory_history_in_currency("AMD", "Utilities", "Cell Phone")
print(res)
