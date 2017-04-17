"""
Computing Sharpe Ratio for momentum strategy
73.7991677066
"""

import pandas as pd
import numpy as np
from collections import OrderedDict
import math

xn_df = pd.read_csv('xn_mom.csv')
r_df = pd.read_csv('all_returns_mom.csv')

year_ago = 253

bmom = OrderedDict([])
bmom['date'] = list(xn_df['date'])
bmom['bmom'] = []
for (key, value) in xn_df.iterrows():
    lst_xn = [float(x) for x in (list(value)[2:])]
    lst_rn = [float(x) for x in list(r_df.ix[key])[2:]]

    xn_rn = []
    for x, r in zip(lst_xn, lst_rn):
        xn_rn.append(x * r)

    bmom['bmom'].append(sum(xn_rn) / (len(xn_rn) - 1))

output = 'bmom.csv'
bmom_df = pd.DataFrame(bmom)
bmom_df.to_csv(output)

bm = bmom['bmom']
daily_avg_return = 1.0/len(bm) * sum(bm)
ann_avg_return = 252 * daily_avg_return
bm_min_daily_avg = [math.pow((b - daily_avg_return), 2) for b in bm]
ann_vol_return = math.sqrt(float(252) /(len(bm) - 1) * sum(bm_min_daily_avg))
SR = ann_avg_return / ann_vol_return
print(SR)

