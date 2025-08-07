""""""
"""
CS7646 P6: indicator_evaluation.  		  	   		  		 			  		 			     			  	 
Student Name: Cheng Hou		  	   		  		 			  		 			     			  	 
GT User ID: chou38 	  	   		  		 			  		 			     			  	 
GT ID: 903141582	  	   		  		 			  		 			     			  	 
"""

import numpy as np
import pandas as pd
import datetime as dt
from util import get_data

def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "chou38"

def compute_sma(prices, sd, ed, lookback):
    dates = pd.date_range(sd, ed)
    prices_norm = prices / prices.ix[0]

    # compute SMA
    sma = prices_norm.rolling(window=lookback, min_periods=lookback).mean()
    sma_ratio = prices_norm / sma

    return sma_ratio

def compute_rsi(prices, sd, ed, lookback):
    dates = pd.date_range(sd, ed)

    # refer to the code on vectorize me slides to compute RSI
    daily_rets = prices.copy()
    daily_rets.values[1:,:] = prices.values[1:,:] - prices.values[:-1,:]
    daily_rets.values[0,:] = np.nan

    up_rets = daily_rets[daily_rets >= 0].fillna(0).cumsum()
    down_rets = -1 * daily_rets[daily_rets < 0].fillna(0).cumsum()

    up_gain = prices.copy()
    up_gain.ix[:,:] = 0
    up_gain.values[lookback:,:] = up_rets.values[lookback:,:] - up_rets.values[:-lookback,:]

    down_loss = prices.copy()
    down_loss.ix[:,:] = 0
    down_loss.values[lookback:,:] = down_rets.values[lookback:,:] - down_rets.values[:-lookback,:]

    rs = (up_gain / lookback) / (down_loss / lookback)
    rsi = 100 - (100 / (1 + rs))
    rsi.ix[:lookback,:] = np.nan
    rsi[rsi == np.inf] = 100

    return rsi

def compute_momentum(prices,sd,ed, lookback):
    # compute momentum
    momentum = prices.pct_change(periods=lookback)

    return momentum