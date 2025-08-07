import indicators as ind
import pandas as pd
from util import get_data

class ManualStrategy(object):
    def __init__(self):
        pass

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "chou38"

    def testPolicy(self, symbol, sd, ed, sv):
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = get_data(syms, dates)
        prices = prices_all[syms]
        prices.fillna(method="ffill")
        prices.fillna(method="bfill")

        # compute the  price/SMA 50 ratio
        sma_ratio = ind.compute_sma(prices, sd, ed, lookback=50)

        # compute RSI
        rsi = ind.compute_rsi(prices, sd, ed, lookback=14)

        # compute momentum
        momentum = ind.compute_momentum(prices, sd, ed, lookback=10)

        # build orders array
        df_trades = prices.copy()
        df_trades.iloc[:] = 0

        position = 0

        for i in range(1, len(prices)):
            sma_value = sma_ratio.iloc[i][0]
            rsi_value = rsi.iloc[i][0]
            momentum_value = momentum.iloc[i][0]
            # buy signal considering SMA, RSI and Momentum

            if sma_value < 0.9 and rsi_value < 30 or rsi_value < 30 and momentum_value > 0 \
                    or sma_value < 0.9 and momentum_value > 0:
                if position == -1000:
                    df_trades.ix[i] = 2000
                    position += 2000
                if position == 0:
                    df_trades.ix[i] = 1000
                    position += 1000
            # sell signal considering SMA, RSI and Momentum
            elif sma_value > 1.1 and rsi_value > 70 or rsi_value > 70 and momentum_value < 0 \
                or sma_value > 1.1 and momentum_value < 0:
                if position == 1000:
                    df_trades.ix[i] = -2000
                    position -= 2000
                if position == 0:
                    df_trades.ix[i] = -1000
                    position -= 1000

        return df_trades