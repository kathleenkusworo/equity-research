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

c1 = Counter()
c2 = Counter()
for (key, dates_lst) in result.iteritems():
    for date in dates_lst:
        mon_year = date[0:7]
        c1[date] += 1
        c2[mon_year] += 1

most_common_20 = c1.most_common(20)
with open('top_20_dates', 'w') as f:
    for (date, num) in most_common_20:
        f.write(date + "\t" + str(num) + "\n")

most_common_50 = c1.most_common(50)
with open('top_50_dates', 'w') as f:
    for (date, num) in most_common_50:
        f.write(date + "\t" + str(num) + "\n")

most_common_20 = c2.most_common(20)
with open('top_20_monyear', 'w') as f:
    for (date, num) in most_common_20:
        f.write(date + "\t" + str(num) + "\n")

most_common_50 = c2.most_common(50)
with open('top_50_monyear', 'w') as f:
    for (date, num) in most_common_50:
        f.write(date + "\t" + str(num) + "\n")
