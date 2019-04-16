from code import util
from engine.TradingModel import TradingModel
import numpy as np
import datetime as dt
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

from colorama import Fore, Style
LOG_COLOR = Style.BRIGHT + Fore.GREEN
ERR_COLOR = Style.BRIGHT + Fore.RED
print(LOG_COLOR + 'using this color for logs')


class RFLearner(TradingModel):
    def __init__(self):
        self.tickers = []
        self.learners = {}

    def addEvidence(self, symbol, data, sd, ed):
        self.sd = sd
        window = 100
        self.window = window
        self.learners[symbol] = RandomForestClassifier(n_estimators=100, max_depth=3)
        values = np.array(data[sd:ed].values)
        values = values.reshape((values.shape[0],))
        #print(values)
        #plt.plot(values)
        #plt.show()

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

        #print(values)
        #print(type(values))
        #plt.plot(values)
        #plt.show()
        #input()

        numdays = (ed - sd).days
        print('numdays', numdays)
        # window = 100
        if numdays < window:
            raise ValueError('Need more days to train Random Forest '
                             'classifier with window ' + str(window))

        trainSamples = []
        labels = []
        for n in range(numdays - window - 1):
            trainVals = values[n : n+window]
            trainSamples.append(trainVals)
            label = 1 if values[n+window+1] > values[n+window] else 0
            labels.append(label)

        self.learners[symbol].fit(trainSamples, labels)


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



