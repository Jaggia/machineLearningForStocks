### Created by Anadi Jaggia
import datetime as dt
import pandas as pd
import util
import indicators
import RTLearner
import BagLearner
import random

def get_X_and_Y(prices, YSELL, YBUY, N, impact):
    df_X = indicators.get_features(prices)
    df_returns = (prices.shift(-N) / prices) - 1.0
    df_Y = indicators.get_Y(df_returns,
                            YSELL - impact,
                            YBUY + impact)
    return df_X, df_Y

class StrategyLearner(object):
    # constructor
    def __init__(self, verbose=False, impact=0.0):
        self.verbose = verbose
        self.impact = impact

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=10000, impact=0):
        # add your code to do learning here

        # N = 5  # Number of day returns to use
        # YSELL = -0.01
        # YBUY = 0.01

        leaf_size = 3  # Leaf size for random tree learner
        n_bags = 20  # Number of bags for baglearner

        syms = [symbol]
        prices_all = util.get_data(syms, pd.date_range(sd, ed))
        prices = prices_all[syms]

        # Calculate indicators and features
        df_X, df_Y = get_X_and_Y(prices, -0.01, 0.01, 7, self.impact)

        Xtrain = df_X.values
        Ytrain = df_Y.values

        self.learner = BagLearner.BagLearner(learner=RTLearner.RTLearner,
                                             kwargs={'leaf_size': leaf_size},
                                             bags=n_bags,
                                             boost=False)
        self.learner.addEvidence(Xtrain, Ytrain)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol="IBM", sd=dt.datetime(2009, 1, 1), ed=dt.datetime(2010, 1, 1), sv=10000):
        syms = [symbol]
        prices_all = util.get_data(syms, pd.date_range(sd, ed))
        prices = prices_all[syms]

        df_X = indicators.get_features(prices)
        Xtest = df_X.values

        Y = self.learner.query(Xtest)

        pos = 0.0
        df_trades = pd.DataFrame(pos,
                                 index=prices.index,
                                 columns=[symbol])

        for i in range(df_trades.shape[0]):
            df_trades[symbol].iloc[i] = Y[i] * 1000.0 - pos
            pos += df_trades[symbol].iloc[i]

        return df_trades
