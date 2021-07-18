import statsmodels.tsa.stattools as ts
import numpy as np
import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt


from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

start = datetime(2014, 12, 1)
end = datetime(2014, 12, 31)


symbols_list=["SPY", "VOO"]

symbols=[]
for ticker in symbols_list: 
    print(ticker)
    #r = web.DataReader(ticker, 'yahoo', start, end)
    r = pdr.get_data_yahoo(ticker, start, end)
    #r = web.DataReader(ticker, 'yahoo', start)
    # add a symbol column
    r['Symbol'] = ticker 
    symbols.append(r)

df = pd.concat(symbols)

df = df.reset_index()
df = df[['Date', 'Adj Close', 'Symbol']] # remove other column
#        Date  Adj Close  Symbol
#0 2020-01-31  92.095001  VWRD.L
#1 2020-02-03  92.605003  VWRD.L
#2 2020-02-04  94.209999  VWRD.L
#3 2020-02-05  94.669998  VWRD.L
#4 2020-02-06  95.180000  VWRD.L

df_pivot = df.pivot('Date','Symbol','Adj Close').dropna()
#df_reshape_by_date_symbol = df.pivot('Date','Symbol','Adj Close')
#df_ret = (df_reshape_by_date_symbol - df_reshape_by_date_symbol.shift(1))/df_reshape_by_date_symbol.shift(1)

(a, pvalue, b) = ts.coint(df_pivot.iloc[:, 0], df_pivot.iloc[:, 1]) 
print(a)
print(pvalue)
print(b)
cut_off = 0.05

if pvalue < cut_off:
    print("cointegration")
else:
    print("not cointegration")

res = df_pivot.iloc[:, 0] - df_pivot.iloc[:, 1]
df_pivot['res'] = res

print(df_pivot.to_string())
df_pivot.plot()
plt.show()
