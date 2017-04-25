import pandas as pd

df = pd.read_csv('arbitrage-portfolio.csv')
unique = (list(df['order_book_id'].unique()))
for i in unique:
    print(i)
