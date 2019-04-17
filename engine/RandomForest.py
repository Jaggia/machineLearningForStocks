import numpy as np
import datetime as dt
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import pandas as pd

from engine.TradingModel import TradingModel
import engine.util as util
from src import indicators

# ySell and yBuy are the min % changes we are looking for
# that will trigger a buy/sell
def get_X_and_Y(prices, YSELL, YBUY, window):
    df_X = indicators.get_features(prices)
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
        window = 100
        self.window = window
        self.learners[symbol] = RandomForestClassifier(n_estimators=100, max_depth=3)

        prices = data[sd:ed]
        # prices = prices.reshape((prices.shape[0],))
        #print(prices)
        print(type(prices))
        #plt.plot(prices)
        #plt.show()
        #input()

        numdays = (ed - sd).days
        print('numdays', numdays)
        # window = 100
        if numdays < window:
            raise ValueError(util.ERR_COLOR + 'Need more days to train Random Forest '
                             'classifier with window ' + str(window))

        # Calculate indicators and features
        prices = util.backfill(prices)
        df_X, df_Y = get_X_and_Y(prices, -0.01, 0.01, 7)
        print(df_X, df_Y)

        Xtrain = df_X.values
        Ytrain = df_Y.values
        Ytrain = Ytrain.reshape((Ytrain.shape[0],))
        print(Xtrain.shape)
        print(Ytrain.shape)

        self.learners[symbol].fit(Xtrain, Ytrain)

        # self.learners[symbol].fit(trainSamples, labels)


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



