import datetime as dt
import marketsimcode as msc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import indicators as ind
from util import get_data

import ManualStrategy as ms
import StrategyLearner as sl


def plot():
    symbol = "JPM"
    syms = [symbol]

    """
    in-sample period
    """

    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000

    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)
    prices = prices_all[syms]
    prices.fillna(method="ffill")
    prices.fillna(method="bfill")

    # build Manual Strategy trades dataframe and compute portvals
    ms_o_in = ms.ManualStrategy()
    ms_df_trades = ms_o_in.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    ms_portvals = msc.compute_portvals(df_trades=ms_df_trades, symbol=symbol,
                                       start_val=sv, commission=9.95, impact=0.005)

    # build benchmark trades dataframe and compuete portvals
    benchmark_df_trades = pd.DataFrame(0, index=ms_df_trades.index, columns=ms_df_trades.columns)
    benchmark_df_trades.ix[0] = 1000
    benchmark_portvals = msc.compute_portvals(df_trades=benchmark_df_trades, symbol=symbol,
                                              start_val=sv, commission=9.95, impact=0.005)

    # build Strategy Learner trades dataframe and compute portvals
    sl_o_in = sl.StrategyLearner()
    sl_o_in.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    sl_df_trades = sl_o_in.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    sl_portvals = msc.compute_portvals(df_trades=sl_df_trades, symbol=symbol,
                                       start_val=sv, commission=9.95, impact=0.005)

    benchmark_portvals_norm = benchmark_portvals / benchmark_portvals.ix[0]
    ms_portvals_norm = ms_portvals / ms_portvals.ix[0]
    sl_portvals_norm = sl_portvals / sl_portvals.ix[0]

    # plot charts
    gen_plot = True
    if gen_plot:
        df_temp = pd.concat(
            [benchmark_portvals_norm, ms_portvals_norm, sl_portvals_norm],
            keys=["Benchmark Values", "Manual Strategy Values", "Strategy Learner Values"], axis=1
        )
        chart = df_temp.plot(
            title="Benchmark vs. Manual Strategy vs. Strategy Learner Portfolio for JPM\n(In-sample Period)",
            linewidth=1, fontsize=8)
        chart.set_xlabel("Date")
        chart.set_ylabel("Normalized Value")
        plt.grid(linestyle='--')
        chart.set_xticks(np.arange(sd, ed, dt.timedelta(90)))
        plt.legend()
        plt.savefig('images/Figure_exp1_in_sample')
        plt.close()
        pass

    """
    out-of-sample period
    """

    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011, 12, 31)
    sv = 100000

    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)
    prices = prices_all[syms]
    prices.fillna(method="ffill")
    prices.fillna(method="bfill")

    # build Manual Strategy trades dataframe and compute portvals
    ms_o_out = ms.ManualStrategy()
    ms_df_trades = ms_o_out.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    ms_portvals = msc.compute_portvals(df_trades=ms_df_trades, symbol=symbol,
                                       start_val=sv, commission=9.95, impact=0.005)

    # build benchmark trades dataframe and compuete portvals
    benchmark_df_trades = pd.DataFrame(0, index=ms_df_trades.index, columns=ms_df_trades.columns)
    benchmark_df_trades.ix[0] = 1000
    benchmark_portvals = msc.compute_portvals(df_trades=benchmark_df_trades, symbol=symbol,
                                              start_val=sv, commission=9.95, impact=0.005)

    # build Strategy Learner trades dataframe and compute portvals
    sl_o_out = sl.StrategyLearner()
    sl_o_out.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    sl_df_trades = sl_o_out.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    sl_portvals = msc.compute_portvals(df_trades=sl_df_trades, symbol=symbol,
                                       start_val=sv, commission=9.95, impact=0.005)

    benchmark_portvals_norm = benchmark_portvals / benchmark_portvals.ix[0]
    ms_portvals_norm = ms_portvals / ms_portvals.ix[0]
    sl_portvals_norm = sl_portvals / sl_portvals.ix[0]

    # plot charts
    gen_plot = True
    if gen_plot:
        df_temp = pd.concat(
            [benchmark_portvals_norm, ms_portvals_norm, sl_portvals_norm],
            keys=["Benchmark Values", "Manual Strategy Values", "Strategy Learner Values"], axis=1
        )
        chart = df_temp.plot(
            title="Benchmark vs. Manual Strategy vs. Strategy Learner Portfolio for JPM\n(Out-of-sample Period)",
            linewidth=1, fontsize=8)
        chart.set_xlabel("Date")
        chart.set_ylabel("Normalized Value")
        plt.grid(linestyle='--')
        chart.set_xticks(np.arange(sd, ed, dt.timedelta(90)))
        plt.legend()
        plt.savefig('images/Figure_exp1_out_of_sample')
        plt.close()
        pass



def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "chou38"

if __name__ == "__main__":
    plot()