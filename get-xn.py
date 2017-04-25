"""
Momentum factor analysis on arbitrage portfolio
"""

import pandas as pd
import numpy as np
from collections import OrderedDict
import math

df = pd.read_csv('all_closing_prices_2016_2017.csv').dropna(axis=1, how='any')

dates = list(df['date'])
all_returns = OrderedDict([])
year_ago = 126
month_ago = 21
N = len(df.columns) - 1
T = (len(df) - year_ago)
all_returns['date'] = dates[year_ago:]

for (key, value) in df.iteritems():
    if (key == 'date'):
        continue
    
    prices = list(value)
    if key not in all_returns:
        all_returns[key] = []
        
    for i in range(year_ago, len(prices)):
        all_returns[key].append(math.log(float(prices[i - month_ago]) / float(prices[i - year_ago])))

output = 'all_returns_mom.csv'
all_returns_df = pd.DataFrame(all_returns)
all_returns_df.to_csv(output)
print("Equity returns written to " + output)

# compute raw factor exposures
x_bar = OrderedDict([])
x_bar['date'] = dates[year_ago:]
x_bar['x_bar'] = []
for (key,value) in all_returns_df.iterrows():
    returns = [float(x) for x in list(value)[1:]]
    x_bar['x_bar'].append(sum(returns)/N)

output = 'x_bar_mom.csv'
x_bar_df = pd.DataFrame(x_bar)
x_bar_df.to_csv(output)
print("X_bar written to " + output)

# cross sectional stdev
stdev = OrderedDict([])
stdev['date'] = dates[year_ago:]
stdev['stdev'] = []
xbar = x_bar['x_bar']
for (i, (key,value)) in enumerate(all_returns_df.iterrows()):
    cur_xbar = xbar[i]
    xraw = list(value)[1:]
    xraw_min_xbar = [(math.pow(float(xr) - cur_xbar, 2)) for xr in xraw]
    stdev['stdev'].append(math.sqrt(sum(xraw_min_xbar)/(N - 1)))

# normalized factor exposures
xn = OrderedDict([])
xn['date'] = dates[year_ago:]
for (key, value) in (all_returns_df.iteritems()):
    if key == 'date':
        continue
    lst_value = [float(x) for x in list(value)]
    for i in range(0, len(lst_value)):
        if key not in xn:
            xn[key] = []

        xn[key].append((lst_value[i] - xbar[i])/stdev['stdev'][i])

output = 'xn_mom.csv'
xn_df = pd.DataFrame(xn)
xn_df.to_csv(output)
print("Normalized factor exposures written to " + output)
