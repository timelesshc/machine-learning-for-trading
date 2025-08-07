""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
import random
import math
  		  	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
import util as ut
import QLearner as ql
import indicators as ind
import marketsimcode as msc
  		  	   		  		 			  		 			     			  	 
class StrategyLearner(object):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			     			  	 
        If verbose = False your code should not generate ANY output.  		  	   		  		 			  		 			     			  	 
    :type verbose: bool  		  	   		  		 			  		 			     			  	 
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 			  		 			     			  	 
    :type impact: float  		  	   		  		 			  		 			     			  	 
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 			  		 			     			  	 
    :type commission: float  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # constructor  		  	   		  		 			  		 			     			  	 
    def __init__(self, verbose=False, impact=0.005, commission=9.95):
        """  		  	   		  		 			  		 			     			  	 
        Constructor method  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        self.verbose = verbose  		  	   		  		 			  		 			     			  	 
        self.impact = impact  		  	   		  		 			  		 			     			  	 
        self.commission = commission
        # actions: LONG (0), CASH (1), SHORT (2)
        self.ql = ql.QLearner(num_states=1000, num_actions=3, alpha=0.2, gamma=0.9, rar=0.5, radr=0.99,dyna=0, verbose=False)
  		  	   		  		 			  		 			     			  	 
    # this method should create a QLearner, and train it for trading  		  	   		  		 			  		 			     			  	 
    def add_evidence(  		  	   		  		 			  		 			     			  	 
        self,  		  	   		  		 			  		 			     			  	 
        symbol,
        sd,
        ed,
        sv,
    ):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Trains your strategy learner over a given time frame.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        :param symbol: The stock symbol to train on  		  	   		  		 			  		 			     			  	 
        :type symbol: str  		  	   		  		 			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			     			  	 
        :type sd: datetime  		  	   		  		 			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			     			  	 
        :type ed: datetime  		  	   		  		 			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
        :type sv: int  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        # add your code to do learning here  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        # example usage of the old backward compatible util function
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		  		 			  		 			     			  	 
        prices_norm = prices / prices.ix[0]

        # compute the  price/SMA ratio
        lookback_sma = 50
        sma_ratio = ind.compute_sma(prices, sd, ed, lookback=lookback_sma)

        # compute RSI
        lookback_rsi = 14
        rsi = ind.compute_rsi(prices, sd, ed, lookback=lookback_rsi)

        # compute momentum
        lookback_momentum = 10
        momentum = ind.compute_momentum(prices, sd, ed, lookback=lookback_momentum)

        # indicator states
        sma_ratio_state = self.discretize(data=sma_ratio,symbol=symbol)
        rsi_state = self.discretize(data=rsi, symbol=symbol)
        momentum_state = self.discretize(data=momentum,symbol=symbol)

        # get initial state
        max_lookback = max(lookback_sma,lookback_rsi,lookback_momentum)
        s_initial = sma_ratio_state[max_lookback] * 100 + rsi_state[max_lookback] * 10 + momentum_state[max_lookback]

        a = self.ql.querysetstate(s_initial)

        iteration = 0
        cr_results = [] # results of cumulative returns

        while iteration < 100:
            if iteration > 20 and cr_results[-1] == cr_results[-2]:
                break

            iteration += 1
            # build orders array
            df_trades = prices.copy()
            df_trades.iloc[:] = 0

            position = 0 # holdings

            for i in range(max_lookback, len(df_trades)-1):
                s = sma_ratio_state[i] * 100 + rsi_state[i] * 10 + momentum_state[i]
                price = prices.iloc[i,0]
                price_next = prices.iloc[i+1,0]
                r = 0  # reward

                if a == 0: # long
                    if position == -1000:
                        df_trades.ix[i] = 2000
                        position += 2000
                        r = - self.impact * (price) * 2000
                    if position == 0:
                        df_trades.ix[i] = 1000
                        position += 1000
                        r = - self.impact * (price) * 1000
                elif a == 1: # cash
                     pass
                else: # short
                    if position == 1000:
                        df_trades.ix[i] = -2000
                        position -= 2000
                        r = - self.impact * (price) * 2000
                    if position == 0:
                        df_trades.ix[i] = -1000
                        position -= 1000
                        r = - self.impact * (price) * 1000

                r += position * (price_next - price)
                a = self.ql.query(s,r)

            portvals = msc.compute_portvals(df_trades=df_trades, symbol=symbol, start_val=sv, commission=self.commission, impact=self.impact)
            cum_ret = portvals[-1] / portvals[0] - 1
            cr_results.append(round(cum_ret,6))


    # this method should use the existing policy and test it against new data  		  	   		  		 			  		 			     			  	 
    def testPolicy(  		  	   		  		 			  		 			     			  	 
        self,  		  	   		  		 			  		 			     			  	 
        symbol,
        sd,
        ed,
        sv,
    ):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Tests your learner using data outside of the training data  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        :param symbol: The stock symbol that you trained on on  		  	   		  		 			  		 			     			  	 
        :type symbol: str  		  	   		  		 			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			     			  	 
        :type sd: datetime  		  	   		  		 			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			     			  	 
        :type ed: datetime  		  	   		  		 			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
        :type sv: int  		  	   		  		 			  		 			     			  	 
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		  		 			  		 			     			  	 
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		  		 			  		 			     			  	 
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		  		 			  		 			     			  	 
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		  		 			  		 			     			  	 
        :rtype: pandas.DataFrame  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        # here we build a fake set of trades  		  	   		  		 			  		 			     			  	 
        # your code should return the same sort of data
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later
        prices_norm = prices / prices.ix[0]

        # compute the  price/SMA ratio
        lookback_sma = 50
        sma_ratio = ind.compute_sma(prices, sd, ed, lookback=lookback_sma)

        # compute RSI
        lookback_rsi = 14
        rsi = ind.compute_rsi(prices, sd, ed, lookback=lookback_rsi)

        # compute momentum
        lookback_momentum = 10
        momentum = ind.compute_momentum(prices, sd, ed, lookback=lookback_momentum)

        # indicator states
        sma_ratio_state = self.discretize(data=sma_ratio, symbol=symbol)
        rsi_state = self.discretize(data=rsi, symbol=symbol)
        momentum_state = self.discretize(data=momentum, symbol=symbol)

        # get initial state
        max_lookback = max(lookback_sma,lookback_rsi,lookback_momentum)
        s_initial = sma_ratio_state[max_lookback] * 100 + rsi_state[max_lookback] * 10 + momentum_state[max_lookback]
        a = self.ql.querysetstate(s_initial)

        # build orders array
        df_trades = prices.copy()
        df_trades.iloc[:] = 0

        position = 0  # holdings

        for i in range(max_lookback, len(df_trades) - 1):
            s = sma_ratio_state[i] * 100 + rsi_state[i] * 10 + momentum_state[i]

            if a == 0:  # long
                if position == -1000:
                    df_trades.ix[i] = 2000
                    position += 2000
                if position == 0:
                    df_trades.ix[i] = 1000
                    position += 1000
            elif a == 1:  # cash
                pass
            else:  # short
                if position == 1000:
                    df_trades.ix[i] = -2000
                    position -= 2000
                if position == 0:
                    df_trades.ix[i] = -1000
                    position -= 1000

            a = self.ql.querysetstate(s)

        return df_trades

    def discretize(self, data, symbol):
        steps = 10 # number of buckets
        temp = data.dropna()
        temp = temp.sort_values(by=symbol)
        step_size = len(temp) / steps
        step_size = math.floor(step_size)
        thresholds = []
        state = []
        for i in range (0, steps):
            thresholds.append(temp.iloc[(i+1)*step_size -1 ][0])

        for index, row in data.iterrows():
            if math.isnan(row[0]):
                state.append(float("NaN"))
            elif row[0] >= max(thresholds):
                state.append(steps - 1)
            elif row[0] <= min(thresholds):
                state.append(0)
            else:
                for i in range (0, steps-1):
                    if thresholds[i] <= row[0] < thresholds[i+1]:
                        state.append(i)

        return state

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "chou38"

if __name__ == "__main__":
    # symbol = "JPM"
    # sd = dt.datetime(2008,1,1)
    # ed = dt.datetime(2009,12,31)
    # sv = 100000
    # sl = StrategyLearner()
    # sl.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    # sl.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    print("One does not simply think up a strategy")
