"""
Computing Sharpe Ratio for momentum strategy
"""

import pandas as pd
import numpy as np
from collections import OrderedDict
import math

xn_df = pd.read_csv('xn_mom.csv')
r_df = pd.read_csv('daily_returns_mom.csv')

year_ago = 126
N = len(xn_df.columns) - 2
T = len(xn_df)

bmom = OrderedDict([])
bmom['date'] = list(xn_df['date'])
bmom['bmom'] = []
for (key, value) in xn_df.iterrows():
    lst_xn = [float(x) for x in (list(value)[2:])]
    lst_rn = [float(x) for x in list(r_df.ix[key])[2:]]

    xn_rn = []
    for x, r in zip(lst_xn, lst_rn):
        xn_rn.append(x * r)

    bmom['bmom'].append(sum(xn_rn) / (N - 1))

output = 'bmom.csv'
bmom_df = pd.DataFrame(bmom)
bmom_df.to_csv(output)

bm = bmom['bmom']
daily_avg_return = 1.0/T * sum(bm)
ann_avg_return = 252 * daily_avg_return
bm_min_daily_avg = [math.pow((b - daily_avg_return), 2) for b in bm]
ann_vol_return = math.sqrt(float(252) /(T - 1) * sum(bm_min_daily_avg))
SR = ann_avg_return / ann_vol_return
print("Sharpe Ratio: " + str(SR))

pn = []

for (key, value) in xn_df.iterrows():
    lst_xn = [float(x) for x in (list(value)[2:])]
    pn.append([x / (N-1) for x in lst_xn])

num_lst = []
for (key, value) in r_df.iterrows():
    lst_rn = [float(x) for x in (list(value)[2:])]
    lst_pn = pn[int(key)]
    
    pn_rn = []
    for p, r in zip(lst_pn, lst_rn):
        pn_rn.append(p * r)
    num_lst.append(sum(pn_rn))
        
num = sum(num_lst)

denom_lst = []
for i in range(1, len(pn)):
    lst_prev = pn[i-1]
    lst_cur = pn[i]

    diff_lst = []
    for prev, cur in zip(lst_prev, lst_cur):
        diff_lst.append(math.fabs(cur - prev))
    denom_lst.append(sum(diff_lst))
denom = sum(denom_lst)

ppt = num/denom
print("Profit per trade: " + str(ppt))

top_rank_lim = math.floor(.4 * N)
low_rank_lim = N - math.floor(.4 * N)

pnrn = OrderedDict([])
for i in range(T):
    xn = xn_df.iloc[[i]]
    rn = r_df.iloc[[i]]

    xn = xn.drop(xn.columns[[0,1]], axis=1)
    rn = rn.drop(rn.columns[[0,1]], axis=1)

    ranked = xn.rank(1, ascending=False)
    pn = 0


    for key in ranked.keys():
        
        if key not in pnrn:
            pnrn[key] = []
            
        if (ranked[key].item() <= top_rank_lim):
            pn = 1
        elif (ranked[key].item() >= low_rank_lim):
            pn = -1
        else:
            pn = 0
        
        pnrn[key].append(pn * rn[key].item())
        
pnrn_df = pd.DataFrame.from_dict(pnrn)
pnrn_df.to_csv('pnrn_ranked.csv')

b_mom = pnrn_df.sum(1)

daily_avg_return = 1.0/T * sum(bm)
ann_avg_return = 252 * daily_avg_return
bm_min_daily_avg = [math.pow((b - daily_avg_return), 2) for b in bm]
ann_vol_return = math.sqrt(float(252) /(T - 1) * sum(bm_min_daily_avg))
SR = ann_avg_return / ann_vol_return
print("Sharpe Ratio (ranked): " + str(SR))

pn = []

for (key, value) in xn_df.iterrows():
    lst_xn = [float(x) for x in (list(value)[2:])]
    pn.append([x / (N-1) for x in lst_xn])

num_lst = []
for (key, value) in r_df.iterrows():
    lst_rn = [float(x) for x in (list(value)[2:])]
    lst_pn = pn[int(key)]
    
    pn_rn = []
    for p, r in zip(lst_pn, lst_rn):
        pn_rn.append(p * r)
    num_lst.append(sum(pn_rn))
        
num = sum(num_lst)

denom_lst = []
for i in range(1, len(pn)):
    lst_prev = pn[i-1]
    lst_cur = pn[i]

    diff_lst = []
    for prev, cur in zip(lst_prev, lst_cur):
        diff_lst.append(math.fabs(cur - prev))
    denom_lst.append(sum(diff_lst))
denom = sum(denom_lst)

ppt = num/denom
print("Profit per trade (ranked): " + str(ppt))

