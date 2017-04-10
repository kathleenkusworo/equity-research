import pandas as pd
import numpy as np
import json
from collections import OrderedDict
from collections import Counter

df = pd.read_csv('3_sigma_returns.csv')

dates = list(df.ix[:,1])
returns = (df.ix[:,2:])

result = OrderedDict([])

for (key,value) in returns.iteritems():
    value_lst = list(value)
    for (i, val) in enumerate(value_lst):
        if not np.isnan(val):
            if key not in result:
                result[key] = []
            result[key].append(dates[i])
    """
    if (not isnull(value)):
        if key not in result:
            result[key] = []
        print(value)
    """
with open('3_sigma_dates.json', 'w') as f:
    json.dump(result,f)

c = Counter()
for (key, dates_lst) in result.iteritems():
    for date in dates_lst:
        c[date] += 1

most_common = c.most_common(20)
with open('top_20_dates', 'w') as f:
    for (date, num) in most_common:
        f.write(date + "\t" + str(num) + "\n")
