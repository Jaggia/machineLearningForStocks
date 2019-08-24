import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from engine import janitor
from engine.TradingModel import TradingModel
import engine.util as util
from src import indicators

# ySell and yBuy are the min % changes we are looking for
# that will trigger a buy/sell
def get_X_and_Y(prices, YSELL, YBUY, window, symbols):
    df_X = indicators.get_features_from_csv(prices, symbols)
    df_returns = (prices.shift(-window) / prices) - 1.0
    df_Y = indicators.get_Y(df_returns,
                            YSELL,
                            YBUY)
    return df_X, df_Y

class RFLearner(TradingModel):
    def __init__(self):
        self.tickers = []
        self.learners = {}

    def addEvidence(self, symbol, data, sd, ed):
        self.sd = sd
        window = 10
        self.window = window
        self.learners[symbol] = RandomForestClassifier(n_estimators=100, max_depth=3)

        numdays = (ed - sd).days
        print('numdays', numdays)
        # window = 100
        if numdays < window:
            raise ValueError(util.ERR_COLOR + 'Need more days to train Random Forest '
                             'classifier with window ' + str(window))

        # Calculate indicators and features
        df_X, df_Y = get_X_and_Y(data, -0.01, 0.01, 7, [symbol])

        df_X = janitor.backfill(df_X)
        df_Y = janitor.backfill(df_Y)

        Xtrain = df_X.values
        Ytrain = df_Y.values
        Ytrain = Ytrain.reshape((Ytrain.shape[0],))
        print(Xtrain.shape)
        print(Ytrain.shape)

        self.learners[symbol].fit(Xtrain, Ytrain)
        print("Feature Importances : ")
        print(self.learners[symbol].feature_importances_)
        # self.learners[symbol].fit(trainSamples, labels)

    def testAndBuildTradingDecisions(self, symbol, data, sd, ed, visualize=False):
        syms = [symbol]
        prices_all = util.get_data(syms, pd.date_range(sd, ed))
        prices = prices_all[syms]
        prices = janitor.backfill(prices)

        df_X, df_Y = get_X_and_Y(prices, -0.01, 0.01, 7)
        df_X = janitor.backfill(df_X)
        Xtest = df_X.values

        # print(df_X)
        Y = self.learners[symbol].predict(Xtest)

        pos = 0.0
        df_trades = pd.DataFrame(pos,
                                 index=prices.index,
                                 columns=[symbol])

        for i in range(df_trades.shape[0]):
            df_trades[symbol].iloc[i] = Y[i] * 1000.0 - pos
            pos += df_trades[symbol].iloc[i]

        #print(Y)
        if visualize:
            pass
            self.visualizeVals()
        return Y

    def visualizeVals(self):
        # how to score? or not necessarily a need for scoring?
        # maybe just a need to measure its performance
        # calculate accuracy measures like alpha, beta etc.
        pass
        # add benchmark which is sp500. just plot its prices
        # so we can compare our performance to the market


    def buyBasedOnPredictions(self, predicatedTrades, currPortfolio):
        print(type(predicatedTrades))

    def trade(self, symbol, data, cd, currency, port):
        # if port > 0:
        #     # either sell 1 stock, do nothing, buy 1 stock
        #     trade = np.random.randint(-1, 2)
        # else:
        #     # either buy 1 stock or do nothin
        #     trade = np.random.randint(0, 2)
        # print('trade', cd, trade)

        values = np.array(data[self.sd:cd].values)
        values = values.reshape((values.shape[0],))

        # replace nans with closest actual price# find closest val
        closestVal = -1
        # find first closestVal
        for n in range(values.shape[0]):
            if str(values[n]) != 'nan':
                closestVal = values[n]
                break

        for n in range(values.shape[0]):
            if str(values[n]) == 'nan':
                values[n] = closestVal
            else:
                closestVal = values[n]

        testSamples = [values[-self.window:]]
        trade = self.learners[symbol].predict(testSamples)
        if trade == 0 and port > 0:
            trade = np.random.randint(-1, 1)  # randomly sell or hold if predicted to drop

        return trade



