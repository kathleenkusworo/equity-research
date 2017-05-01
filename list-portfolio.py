import pandas as pd

def print_lst(lst):
    for (order_book_id, symbol) in lst:
        print(symbol + " (" + order_book_id + ")")

df = pd.read_csv('arbitrage-portfolio.csv')
equities_df = df[df['order_book_id'].str.contains('XSHE') | df['order_book_id'].str.contains('XSHG')][['order_book_id', 'symbol']]

equities_lst = []
for (key, value) in equities_df.iterrows():
    to_be_added = (value['order_book_id'], value['symbol'])
    if to_be_added not in equities_lst:
        equities_lst.append(to_be_added)

print_lst(equities_lst)


one_letter = {'A': 'Soybean', 'M': 'Soybean meal', 'Y': 'Soybean oil', 'C': 'Corn', 'L': 'LLDPE', 'P': 'Palm oil', 'V': 'PVC', 'J': 'Coke', 'I': 'Iron Ore', 'R': 'Rapeseed oil'}

two_letters = {'JM': 'Coking coal', 'FB': 'Fiber plate', 'PP': 'Polypropylene', 'JD': 'Egg', 'BB': 'Rubber', 'JR': 'Japonica'}

futures_df = df[~(df['order_book_id'].str.contains('XSHE') | df['order_book_id'].str.contains('XSHG'))][['order_book_id', 'symbol']]

futures_lst = list(futures_df['order_book_id'].unique())
for order_id in futures_lst:
    first_two = order_id[0:2]
    first_one = order_id[0:1]
    if first_two in two_letters:
        print(order_id + " (" + two_letters[first_two] + ")")
    elif first_one in one_letter:
        print(order_id + " (" + one_letter[first_one] + ")")
    else:
        print(order_id)
        
