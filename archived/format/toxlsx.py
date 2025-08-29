import pandas as pd

pd.read_csv("cards.csv").to_excel("cards.xlsx", index=False)
