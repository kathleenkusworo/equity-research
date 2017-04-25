from collections import OrderedDict
from math import log
import pandas as pd
import numpy as np

def get_index_from_date(df, value):
    # print(value)
    return df[df['Date'] == value].index.tolist()[0]

all_closing_prices = pd.read_csv('all_closing_prices.csv').dropna(axis=1, how='any')
all_volumes = pd.read_csv('all_volumes.csv').dropna(axis=1, how='any')
sp500_china = pd.read_csv('sp500_china.csv')
# print(sp500_china[sp500_china['Date'] == '2014'].index)
# print(len(all_closing_prices.columns))
all_returns = OrderedDict([])
all_means = OrderedDict([])
all_stdev = OrderedDict([])
col_num = 0

dates = []
for (key, value) in all_closing_prices.iteritems():
    value_dict = dict(value)
    if (col_num == 0):
        dates = list(value_dict.values()) # first entry is 2014/1/2
    else:
        prices = list(value_dict.values())
        # compute daily log returns for each stock
        returns = OrderedDict([])
        for i in range(0, len(prices) - 1):
            returns[i+1] = log(float(prices[i + 1]) / float(prices[i])) - sp500_china['Return'][get_index_from_date(sp500_china, dates[i+1])]
        all_returns[key] = returns
    
        # compute mean of returns
        return_vals = list(returns.values())
        all_means[key] = np.mean(return_vals)
    
        # compute stdev of returns
        all_stdev[key] = np.std(return_vals)

    col_num += 1

# In[9]:

all_upper_lim = OrderedDict([])
all_lower_lim = OrderedDict([])

for key in all_means.keys():
    all_upper_lim[key] = all_means[key] + 3 * all_stdev[key]
    all_lower_lim[key] = all_means[key] - 3 * all_stdev[key]

all_three_sigma_returns = OrderedDict([])
all_three_sigma_volumes = OrderedDict([])

all_three_sigma_returns['Date'] = []
all_three_sigma_volumes['Date'] = []

for i in range(len(dates)):
    all_three_sigma_returns['Date'].append(dates[i])
    all_three_sigma_volumes['Date'].append(dates[i])

for key, value in all_returns.items():
    all_three_sigma_returns[key] = [np.NaN for i in range(len(dates))]
    all_three_sigma_volumes[key] = [np.NaN for i in range(len(dates))]
    upper_lim = all_upper_lim[key]
    lower_lim = all_lower_lim[key]
    for date, return_value in value.items():
        if return_value > upper_lim or return_value < lower_lim:
            all_three_sigma_returns[key][date] = return_value
            all_three_sigma_volumes[key][date] = all_volumes[key][date]


pd.DataFrame(all_three_sigma_returns).to_csv('3_sigma_returns.csv')
pd.DataFrame(all_three_sigma_volumes).to_csv('3_sigma_volumes.csv')

# In[ ]:



