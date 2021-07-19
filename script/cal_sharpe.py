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

def cal_sharpe(df):

    df['daily_ret'] = df['Adj Close'].pct_change()
    df = df.dropna()

    rfr = 0.02
    df['excess_daily_ret'] = df['daily_ret'] - rfr/len(df.index)
    return annualised_sharpe(df, len(df.index))

def annualised_sharpe(df, N=252):
    mean = df['excess_daily_ret'].mean()
    std = df['daily_ret'].std()
    print("len %s", N)
    print("mean %s", mean)
    print("std %s", std) 
    return np.sqrt(N) * mean / std

yf.pdr_override()

start = datetime(2020, 2, 1)
end = datetime(2021, 6, 30)
#symbols_list = ["GBTC", "IDNA","SMH", "ICLN","ARKF", "ARKK", "CIBR", "WCLD", "VT", "VTI", "QQQ", "VXF","VEU", "VWO", "BLV", "BIV", "BSV", "VNQ", "BNDX", "BND", "LQD","VTIP", "VNQI", "DBC", "HYG", "GLD", "VCIT", "VGIT", "VCSH", "VGSH"]

#symbols_list=["BLV", "ARKK", "VNQ", "VNQI", "QQQ", "DBC", "GLD", "VTI", "VDE"]
#symbols_list=["VTI", "VT", "QQQ", "BLV", "VIRT", "KIND-SDB.ST", "ADM.L", "VWO", "SMT.L", "ARKK"]
symbols_list=["VTI", "VT", "VIRT", "ARKK", "ADM.L", "VWO", "SMT.L", "BLV"]


#pull price using iex for each symbol in list defined above
for ticker in symbols_list: 
    print(ticker)
    #r = web.DataReader(ticker, 'yahoo', start, end)
    r = pdr.get_data_yahoo(ticker, start, end)
    #r = web.DataReader(ticker, 'yahoo', start)
    # add a symbol column
    r['Symbol'] = ticker	
    
    df = r.dropna()
    print("sharpe ratio for %s is %s" %(ticker, cal_sharpe(df)))	
