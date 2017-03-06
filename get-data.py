from collections import OrderedDict
from math import log
import pandas as pd
import numpy as np

all_closing_prices = pd.read_csv('all_closing_prices.csv').dropna(axis=1, how='any')
all_volumes = pd.read_csv('all_volumes.csv').dropna(axis=1, how='any')

all_returns = OrderedDict([])
all_means = OrderedDict([])
all_stdev = OrderedDict([])
col_num = 0

dates = []
for (key, value) in all_closing_prices.iteritems():
    value_dict = dict(value)
    if (col_num == 0):
        dates = list(value_dict.values())
    else:
        prices = list(value_dict.values())
        if (col_num == 1):
            print(prices)
        # compute daily log returns for each stock
        returns = OrderedDict([])
        for i in range(0, len(prices) - 1):
            returns[i] = log(float(prices[i + 1]) / float(prices[i]))
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

all_three_sigma = OrderedDict([])

for key, value in all_returns.items():
    all_three_sigma[key] = OrderedDict([])
    all_three_sigma[key]['return'] = OrderedDict([])
    all_three_sigma[key]['volume'] = OrderedDict([])
    upper_lim = all_upper_lim[key]
    lower_lim = all_lower_lim[key]
    for date, return_value in value.items():
        if return_value <= upper_lim and return_value >= lower_lim:
            all_three_sigma[key]['return'][date] = return_value
            all_three_sigma[key]['volume'][date] = all_volumes[key][date]


result = pd.DataFrame(all_three_sigma)
result.to_csv('result.csv')
# In[ ]:



