from src import util
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
        self.learners[symbol] = RandomForestClassifier()
        values = np.array(data[sd:ed].values)
        values = values.reshape((values.shape[0],))
        plt.plot(values)
        plt.show()

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

        plt.plot(values)
        plt.show()
        print(values)
        # input()

    def trade(self, symbol, data, sd, ed, currency):
        pass


