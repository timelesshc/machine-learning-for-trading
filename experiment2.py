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

    # build Strategy Learner trades dataframe and compute portvals

    # impact = 0
    sl_o_impact1 = sl.StrategyLearner(impact=0,commission=0)
    sl_o_impact1.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    sl_df_trades_impact1 = sl_o_impact1.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    num_trades_impact1 = np.count_nonzero(sl_df_trades_impact1)
    sl_portvals_impact1 = msc.compute_portvals(df_trades=sl_df_trades_impact1, symbol=symbol,
                                       start_val=sv, commission=0, impact=0)
    sl_portvals_norm_impact1 = sl_portvals_impact1 / sl_portvals_impact1.ix[0]

    # impact = 0.02
    sl_o_impact2 = sl.StrategyLearner(impact=0.02,commission=0)
    sl_o_impact2.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    sl_df_trades_impact2 = sl_o_impact2.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    num_trades_impact2 = np.count_nonzero(sl_df_trades_impact2)
    sl_portvals_impact2 = msc.compute_portvals(df_trades=sl_df_trades_impact2, symbol=symbol,
                                       start_val=sv, commission=0, impact=0.02)
    sl_portvals_norm_impact2 = sl_portvals_impact2 / sl_portvals_impact2.ix[0]

    # impact = 0.05
    sl_o_impact3 = sl.StrategyLearner(impact=0.05,commission=0)
    sl_o_impact3.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    sl_df_trades_impact3 = sl_o_impact3.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    num_trades_impact3 = np.count_nonzero(sl_df_trades_impact3)
    sl_portvals_impact3 = msc.compute_portvals(df_trades=sl_df_trades_impact3, symbol=symbol,
                                       start_val=sv, commission=0, impact=0.05)
    sl_portvals_norm_impact3 = sl_portvals_impact3 / sl_portvals_impact3.ix[0]

    # plot charts
    gen_plot = True
    if gen_plot:
        df_temp = pd.concat(
            [sl_portvals_norm_impact1, sl_portvals_norm_impact2, sl_portvals_norm_impact3],
            keys=["Impact = 0", "Impact = 0.02", "Impact = 0.05"], axis=1
        )
        chart = df_temp.plot(
            title="Impact vs. Strategy Learner Portfolio for JPM\n(In-sample Period)",
            linewidth=1, fontsize=8)
        chart.set_xlabel("Date")
        chart.set_ylabel("Normalized Value")
        plt.grid(linestyle='--')
        chart.set_xticks(np.arange(sd, ed, dt.timedelta(90)))
        plt.legend()
        plt.savefig('images/Figure_exp2_values')
        plt.close()


        data = {"0":num_trades_impact1, "0.02":num_trades_impact2, "0.05":num_trades_impact3}
        impact = list(data.keys())
        trades = list(data.values())

        plt.bar(impact, trades)
        plt.xlabel("Impact")
        plt.ylabel("Number of trades")
        plt.title("Impact vs. Number of Trades for JPM\n(In-sample Period)")
        plt.grid(linestyle='--')
        plt.savefig('images/Figure_exp2_trades')
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