"""
Get all equities in Runkai's arbitrage portfolio
"""
import pandas as pd
import numpy as np
from collections import OrderedDict

df = pd.read_csv('arbitrage-portfolio.csv')
equities = df[df['order_book_id'].str.contains('XSHE') | df['order_book_id'].str.contains('XSHG')]['order_book_id']

print(list(equities))
