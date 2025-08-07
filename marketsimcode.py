""""""  		  	   		  		 			  		 			     			  	 
"""MC2-P1: Market simulator.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Student Name: Cheng Hou		  	   		  		 			  		 			     			  	 
GT User ID: chou38 	  	   		  		 			  		 			     			  	 
GT ID: 903141582	  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import datetime as dt  		  	   		  		 			  		 			     			  	 
import os  		  	   		  		 			  		 			     			  	 
import math
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data
  		  	   		  		 			  		 			     			  	 
def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "chou38"

def compute_portvals(  		  	   		  		 			  		 			     			  	 
    df_trades,
    symbol,
    start_val,
    commission,
    impact,
):

    # build Prices dataframe
    syms = [symbol]
    start_date = min(df_trades.index)
    end_date = max(df_trades.index)
    dates = pd.date_range(start_date, end_date)

    prices_all = get_data(syms, dates)
    prices = prices_all[syms]
    prices.fillna(method="ffill")
    prices.fillna(method="bfill")
    prices_df = prices.assign(Cash= 1.0)

    # build Trade dataframe (include transaction cost)
    transaction_cost = prices * df_trades * impact
    transaction_cost.columns=["Cost"]
    transaction_cost[df_trades != 0]= transaction_cost + commission
    df_trades = df_trades.assign(Cash=(prices * df_trades).sum(axis=1) * -1)
    df_trades.loc[:, "Cash"] = df_trades.loc[:, "Cash"] - transaction_cost.loc[:, "Cost"]

    # build Holdings dataframe
    holdings_df = df_trades.copy()
    prev_date = start_date
    for date in holdings_df.index:
        if date == holdings_df.index[0]:
            holdings_df.loc[date, "Cash"] = holdings_df.loc[date, "Cash"] + start_val
            continue
        holdings_df.loc[date,:] = holdings_df.loc[prev_date,:] + df_trades.loc[date, :]
        prev_date = date

    # build Values dataframe
    values_df = prices_df * holdings_df
    portvals = values_df.sum(axis=1)

    return portvals  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def compare_perform_metrics(ms_portvals, benchmark_portvals):
    # compute cumulative return (cr)
    cum_ret = ms_portvals.iloc[-1] / ms_portvals.iloc[0] - 1
    # compute portfolio average daily return (adr)
    daily_returns = ms_portvals / ms_portvals.shift(1) - 1
    daily_returns = daily_returns[1:]
    avg_daily_ret = daily_returns.mean()
    # compute portfolio Standard deviation of daily return (sddr)
    std_daily_ret = daily_returns.std()
    # compute sharpe ratio (sr) given 252 trading days in a year and daly risk free return = 0
    sharpe_ratio = math.sqrt(252) * avg_daily_ret / std_daily_ret

    # compute cumulative return (cr)
    cum_ret_benchmark = benchmark_portvals.iloc[-1] / benchmark_portvals.iloc[0] - 1
    # compute portfolio average daily return (adr)
    daily_returns_benchmark = benchmark_portvals / benchmark_portvals.shift(1) - 1
    daily_returns_benchmark = daily_returns_benchmark[1:]
    avg_daily_ret_benchmark = daily_returns_benchmark.mean()
    # compute portfolio Standard deviation of daily return (sddr)
    std_daily_ret_benchmark = daily_returns_benchmark.std()
    # compute sharpe ratio (sr) given 252 trading days in a year and daly risk free return = 0
    sharpe_ratio_benchmark = math.sqrt(252) * avg_daily_ret_benchmark / std_daily_ret_benchmark

    print(f"Cumulative Return of Manual Strategy: {'%.6f' % cum_ret}")
    print(f"Cumulative Return of Benchmark : {'%.6f' % cum_ret_benchmark}")
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Standard Deviation of Manual Strategy: {'%.6f' % std_daily_ret}")
    print(f"Standard Deviation of Benchmark : {'%.6f' % std_daily_ret_benchmark}")
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return of Manual Strategy: {'%.6f' % avg_daily_ret}")
    print(f"Average Daily Return of Benchmark : {'%.6f' % avg_daily_ret_benchmark}")
