import ManualStrategy as ms
import StrategyLearner as sl
import datetime as dt
import marketsimcode as msc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import indicators as ind
from util import get_data
import experiment1 as exp1
import experiment2 as exp2

def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "chou38"

if __name__ == "__main__":
    symbol = "JPM"
    syms = [symbol]
    """
    in-sample period
    """

    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000

    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)
    prices = prices_all[syms]
    prices.fillna(method="ffill")
    prices.fillna(method="bfill")

    # build Manual Strategy trades datafram and compute portvals
    ms = ms.ManualStrategy()
    ms_df_trades = ms.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)

    """ Check orders
    for i in range(0,len(ms_df_trades)):
        if ms_df_trades.iloc[i][0] != 0:
            print(ms_df_trades.iloc[i][0])
    """

    ms_portvals = msc.compute_portvals(df_trades=ms_df_trades, symbol=symbol,
                                      start_val=sv, commission=9.95, impact=0.005)

    # build benchmark trades dataframe and compuete portvals
    benchmark_df_trades = pd.DataFrame(0, index=ms_df_trades.index, columns=ms_df_trades.columns)
    benchmark_df_trades.ix[0] = 1000
    benchmark_portvals = msc.compute_portvals(df_trades=benchmark_df_trades,symbol=symbol,
                                             start_val=sv,commission=9.95,impact=0.005)

    # plot charts
    gen_plot = True
    ms_portvals_norm = ms_portvals / ms_portvals.ix[0]
    benchmark_portvals_norm = benchmark_portvals / benchmark_portvals.ix[0]
    if gen_plot:
        df_temp = pd.concat(
            [ms_portvals_norm, benchmark_portvals_norm],
            keys=["Manual Strategy Values", "Benchmark Values"], axis=1
        )
        chart = df_temp.plot(title = "Manual Strategy Portfolio vs. Benchmark Portfolio for JPM\n(In-sample Period)", linewidth=1, color=["red","purple"] , fontsize = 8)
        chart.set_xlabel("Date")
        chart.set_ylabel("Normalized Value")
        plt.grid(linestyle='--')
        chart.set_xticks(np.arange(sd,ed, dt.timedelta(90)))

        # add vertical lines to indicate long/short entry points
        long_line_count = 0
        short_line_count = 0
        for i in ms_df_trades.index:
            if long_line_count == 0:
                if ms_df_trades.loc[i][0] > 0:
                    plt.axvline(x=i, color='blue', label='Long Entry Point')
                    long_line_count += 1
            else:
                if ms_df_trades.loc[i][0] > 0:
                    plt.axvline(x=i, color='blue')

            if short_line_count == 0:
                 if ms_df_trades.loc[i][0] < 0:
                    plt.axvline(x=i, color='black', label='Short Entry Point')
                    short_line_count += 1
            else:
                if ms_df_trades.loc[i][0] < 0:
                    plt.axvline(x=i, color='black')
        plt.legend()
        plt.savefig('images/Figure_ms_in_sample')
        plt.close()
        pass

    # compare performance metrics
    gen_metrics = False
    if gen_metrics:
        print('In-sample Period Statistics:')
        msc.compare_perform_metrics(ms_portvals, benchmark_portvals)

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

    # build Manual Strategy trades datafram and compute portvals
    ms_df_trades = ms.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    ms_portvals = msc.compute_portvals(df_trades=ms_df_trades, symbol=symbol,
                                       start_val=sv, commission=9.95, impact=0.005)

    # build benchmark trades dataframe and compuete portvals
    benchmark_df_trades = pd.DataFrame(0, index=ms_df_trades.index, columns=ms_df_trades.columns)
    benchmark_df_trades.ix[0] = 1000
    benchmark_portvals = msc.compute_portvals(df_trades=benchmark_df_trades, symbol=symbol,
                                              start_val=sv, commission=9.95, impact=0.005)

    # plot charts
    ms_portvals_norm = ms_portvals / ms_portvals.ix[0]
    benchmark_portvals_norm = benchmark_portvals / benchmark_portvals.ix[0]
    if gen_plot:
        df_temp = pd.concat(
            [ms_portvals_norm, benchmark_portvals_norm],
            keys=["Manual Strategy Values", "Benchmark Values"], axis=1
        )
        chart = df_temp.plot(title="Manual Strategy Portfolio vs. Benchmark Portfolio for JPM\n(Out-of-sample Period)", linewidth=1,
                             color=["red", "purple"], fontsize=8)
        chart.set_xlabel("Date")
        chart.set_ylabel("Normalized Value")
        plt.grid(linestyle='--')
        chart.set_xticks(np.arange(sd, ed, dt.timedelta(90)))

        # add vertical lines to indicate long/short entry points
        long_line_count = 0
        short_line_count = 0
        for i in ms_df_trades.index:
            if long_line_count == 0:
                if ms_df_trades.loc[i][0] > 0:
                    plt.axvline(x=i, color='blue', label='Long Entry Point')
                    long_line_count += 1
            else:
                if ms_df_trades.loc[i][0] > 0:
                    plt.axvline(x=i, color='blue')

            if short_line_count == 0:
                 if ms_df_trades.loc[i][0] < 0:
                    plt.axvline(x=i, color='black', label='Short Entry Point')
                    short_line_count += 1
            else:
                if ms_df_trades.loc[i][0] < 0:
                    plt.axvline(x=i, color='black')
        plt.legend()
        plt.savefig('images/Figure_ms_out_of_sample')
        plt.close()
        pass

    # compare performance metrics
    if gen_metrics:
        print('Out-of-sample Period Statistics:')
        msc.compare_perform_metrics(ms_portvals, benchmark_portvals)

    # conduct experiment 1
    exp1.plot()

    # conduct experiment 2
    exp2.plot()


