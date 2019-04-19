### Created by Anadi Jaggia
import datetime as dt
import pandas as pd
from engine import util
from engine import RandomForest
from src import indicators
from src import RTLearner
from src import BagLearner
from engine import janitor


def get_X_and_Y(prices, YSELL, YBUY, N, impact):
    df_X = indicators.get_features(prices)
    df_returns = (prices.shift(-N) / prices) - 1.0
    df_Y = indicators.get_Y(df_returns,
                            YSELL - impact,
                            YBUY + impact)
    return df_X, df_Y


def get_X_and_Y_test(prices, YSELL, YBUY, N, impact):
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
    # ALEX I removed default values to make the first 3 arguments required
    def addEvidence(self, symbol, sd, ed, sv=10000, impact=0):
        # add your classCode to do learning here

        # N = 5  # Number of day returns to use
        # YSELL = -0.01
        # YBUY = 0.01

        leaf_size = 3  # Leaf size for random tree learner
        n_bags = 20  # Number of bags for baglearner

        syms = [symbol]
        prices_all = util.get_data(syms, pd.date_range(sd, ed))
        prices = prices_all[syms]

        prices = janitor.backfill(prices)
        # Calculate indicators and features
        df_X, df_Y = get_X_and_Y(prices, -0.001, 0.001, 7, self.impact)

        df_X = janitor.cleanWithZeros(df_X)
        df_Y = janitor.cleanWithZeros(df_Y)

        Xtrain = df_X.values
        Ytrain = df_Y.values

        # self.learner = BagLearner.BagLearner(learner=RTLearner.RTLearner,
        #                                      kwargs={'leaf_size': leaf_size},
        #                                      bags=n_bags,
        #                                      boost=False)
        self.learner = RTLearner.RTLearner(leaf_size=leaf_size)
        # self.learner = RandomForest.RFLearner() # Didn't wanna change this b4 you see this
        self.learner.addEvidence(Xtrain=Xtrain, Ytrain=Ytrain)
        self.sd = sd

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol, sd, ed, sv=10000):
        # cd = sd
        # Y = None
        # while cd < ed:
        #     print('Trading for day ', cd)
        #
        #     syms = [symbol]
        #     prices_all = util.get_data(syms, pd.date_range(self.sd, cd))
        #     prices = prices_all[syms]
        #
        #     prices = janitor.backfill(prices)
        #     # Calculate indicators and features
        #     df_X, df_Y = get_X_and_Y_test(prices, -0.01, 0.01, 7, self.impact)
        #
        #     df_X = janitor.backfill(df_X)
        #
        #     Xtest = df_X.values
        #
        #
        #     #Y = self.learner.query(Xtest, symbol, prices.index)
        #     trades = self.learner.query(Xtest, symbol, prices.index)
        #     if Y is None:
        #         Y = trades[trades.index == cd]
        #     else:
        #         Y = pd.concat([Y, trades[trades.index == cd]])
        #
        #     cd += dt.timedelta(days=1)

        syms = [symbol]
        prices_all = util.get_data(syms, pd.date_range(self.sd, ed))
        prices = prices_all[syms]

        prices = janitor.backfill(prices)
        # Calculate indicators and features
        df_X, df_Y = get_X_and_Y_test(prices, -0.01, 0.01, 7, self.impact)

        df_X = janitor.backfill(df_X)

        Xtest = df_X.values


        #Y = self.learner.query(Xtest, symbol, prices.index)
        Y = self.learner.query(Xtest, symbol, prices.index)

        return Y
        #return df_trades
