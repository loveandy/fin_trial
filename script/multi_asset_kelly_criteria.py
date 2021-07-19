import numpy as np
import pandas as pd
#used to grab the stock prices, with yahoo
import pandas_datareader as web
from datetime import datetime
#to visualize the results
import matplotlib.pyplot as plt
import seaborn
import sys

from scipy import stats

from pandas import DataFrame
from numpy.linalg import inv

from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

start = datetime(2020, 1, 1)
end = datetime(2021, 6, 30)
symbols_list=["VOO", "QQQ", "IWM", "VGK", "EWJ", "VWO", "GSG", "GLD", "VNQ", "HYG", "TLT", "LQD", "IEF"]
future_ret = {"VOO":0.05, "QQQ":0.07, "IWM":0.03, "VGK":0.02, "EWJ":0.02, "VWO":0.02, "GSG":0.01, "GLD":0.01, "VNQ":0.025, "HYG":0.025, "TLT":-0.02, "LQD":0.01, "IEF":0.01}

#symbols_list=["VOO", "QQQ"]
year_rfr = 0.02
daily_rfr = year_rfr/252

ret = {}
excess_return = {}

#pull price using iex for each symbol in list defined above
for ticker in symbols_list: 
    print(ticker)
    r = pdr.get_data_yahoo(ticker, start, end)
    # add a symbol column
    r['Symbol'] = ticker
    ret[ticker] = r['Adj Close'].pct_change()
    excess_return[ticker] = (ret[ticker] - daily_rfr)


df = DataFrame(excess_return).dropna()
print(df.head())

# Calculate the CoVariance and Mean of the DataFrame
C = 252 * df.cov()
#print(inv(C))

# use geometric mean if possible. otherwise, use arithmetic mean when total return is negative
rslt = {}
for col in df:
    #print(col)
    total_ret = np.cumprod(df[col]+1)[-1]
    #print(total_ret)
    daily_ret = 0
    if total_ret > 1:
        #print(1/len(df[col]))
        daily_ret = pow(total_ret, 1/len(df[col])) - 1
    else:
        daily_ret = df[col].mean()
    #print("%s %s" %(col, daily_ret*252))
    rslt[col] = daily_ret*252

# use arith mean
#M = 252 * df.mean()

# use gmean
#M = pd.Series(rslt)

# use expected future return
M = pd.Series(future_ret)
print(M)
#M = np.power( stats.gmean(df)+1, 252)

#corr = df.corr()
#print(corr)

# Calculate the Kelly-Optimal Leverages using Matrix Multiplication
# refer to https://www.frontiersin.org/articles/10.3389/fams.2020.577050/full (12)
F = inv(C).dot(M)

sum = 0
print("unconstrainted leverage")
ex_ret = 0
for security, leverage in zip(df.columns.values.tolist(), F):
    print("weight %s for %s" %(leverage, security))
    sum += leverage
    ex_ret += leverage*M[security]
print("total weight %s" %(sum))
print("ex ret %s" %(ex_ret))

leverage_limit = 1.5

if sum > leverage_limit:
    new_sum = 0
    expected_return = 0
    for security, leverage in zip(df.columns.values.tolist(), F):
        print("weight %s for %s" %(leverage/sum*leverage_limit, security))
        new_sum += leverage/sum*leverage_limit
        expected_return += leverage/sum*leverage_limit * M[security]
        #print(expected_return)
    print("new total weight %s" %(new_sum))
    print("expected return %s" %(expected_return))
