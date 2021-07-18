import numpy as np
import pandas as pd
#used to grab the stock prices, with yahoo
import pandas_datareader as web
from datetime import datetime
#to visualize the results
import matplotlib.pyplot as plt
import seaborn
import sys

from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

start = datetime(2020, 2, 1)
end = datetime(2020, 6, 30)
#symbols_list = ["GBTC", "IDNA","SMH", "ICLN","ARKF", "ARKK", "CIBR", "WCLD", "VT", "VTI", "QQQ", "VXF","VEU", "VWO", "BLV", "BIV", "BSV", "VNQ", "BNDX", "BND", "LQD","VTIP", "VNQI", "DBC", "HYG", "GLD", "VCIT", "VGIT", "VCSH", "VGSH"]

#symbols_list=["BLV", "ARKK", "VNQ", "VNQI", "QQQ", "DBC", "GLD", "VTI", "VDE"]
#symbols_list=["VTI", "VT", "QQQ", "BLV", "VIRT", "KIND-SDB.ST", "ADM.L", "VWO", "SMT.L", "ARKK"]
symbols_list=["VTI", "VT", "VIRT", "ARKK", "ADM.L"]
#symbols_list=["VOO", "QQQ", "IWM", "VGK", "EWJ", "GSG", "GLD", "VNQ", "HYG", "TLT", "LQD", "IEF", "SHY"]
#symbols_list=["VTI","VT", "VNQ", "VNQI", "TLT", "GSG", "GLD", "TIP", "VIRT"]
#symbols_list=["VTI", "DEEP", "GVAL", "QVAL", "IVAL", "FVAL", "DSTL", "NULV", "SLVY", "IWS", "VTV"]
#symbols_list=["VTI", "PSP", "PEX"]
symbols=[]

#pull price using iex for each symbol in list defined above
for ticker in symbols_list: 
    print(ticker)
    #r = web.DataReader(ticker, 'yahoo', start, end)
    r = pdr.get_data_yahoo(ticker, start, end)
    #r = web.DataReader(ticker, 'yahoo', start)
    # add a symbol column
    r['Symbol'] = ticker 
    symbols.append(r)
#print(symbols)

df = pd.concat(symbols)
df.dropna()


df = df.reset_index()
df = df[['Date', 'Adj Close', 'Symbol']] # remove other column
#        Date  Adj Close  Symbol
#0 2020-01-31  92.095001  VWRD.L
#1 2020-02-03  92.605003  VWRD.L
#2 2020-02-04  94.209999  VWRD.L
#3 2020-02-05  94.669998  VWRD.L
#4 2020-02-06  95.180000  VWRD.L

df_reshape_by_date_symbol = df.pivot('Date','Symbol','Adj Close')

print(df_reshape_by_date_symbol.iloc[0])
print(df_reshape_by_date_symbol.iloc[-1])
ret = (df_reshape_by_date_symbol.iloc[-1]-df_reshape_by_date_symbol.iloc[0])/df_reshape_by_date_symbol.iloc[0]

# return in the sampling period
print(ret)

# calculate correction by log return
df_ret = (df_reshape_by_date_symbol/df_reshape_by_date_symbol.shift())
print(df_ret.to_string())
df_ret = df_ret.dropna()
df_ret = np.log(df_ret)

# calculate correction by price
#df_ret = df_reshape_by_date_symbol 

df_pivot = df_ret.dropna().reset_index()

print(df_pivot)


#df_pivot = df.pivot('Date','Symbol','Adj Close').reset_index()
# reshape the dataframe with index by "Date" and column by "Symbol" and then reset index
#Symbol            BIV        BLV        BSV    DBC       VIRT        VNQ     VWRD.L
#Date
#2020-01-31  85.648407  97.973213  79.387413  14.58  15.715295  88.971741  92.095001
#2020-02-03  85.549515  98.066162  79.370789  14.31  15.470478  89.265366  92.605003
#2020-02-04  85.232666  97.173820  79.243637  14.33  16.233175  90.184166  94.209999
#2020-02-05  85.050217  96.606796  79.175179  14.55  16.336750  90.240997  94.669998
#2020-02-06  85.069420  96.839180  79.175179  14.61  15.724711  90.544113  95.180000



corr_df = df_pivot.corr(method='spearman')
#reset symbol as index (rather than 0-X)
corr_df.head().reset_index()
#del corr_df.index.name
corr_df = corr_df.rename_axis(None, axis=1)
print(corr_df.head(10))

#take the bottom triangle since it repeats itself
mask = np.zeros_like(corr_df)
#mask[np.triu_indices_from(mask)] = True
#generate plot
seaborn.heatmap(corr_df, cmap='RdYlGn', vmax=1.0, vmin=-1.0 , mask = mask, linewidths=2.5)
plt.yticks(rotation=0) 
plt.xticks(rotation=90) 
plt.show()
