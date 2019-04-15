from code import util
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from engine.RandomForest import RFLearner

from colorama import Fore, Style
LOG_COLOR = Style.BRIGHT + Fore.GREEN
ERR_COLOR = Style.BRIGHT + Fore.RED
print(LOG_COLOR + 'using this color for logs')


class Simulation(object):
    def __init__(self,
                 sd_train=dt.datetime(2009, 1, 1),
                 sd_test=dt.datetime(2010, 1, 1),
                 ed_test=dt.datetime(2011, 1, 1),
                 currency=10000,
                 model=RFLearner(),
                 tickers=('GOOG', 'MSFT',)):# 'AMZN', 'IBM', 'AAPL')):

        self.sd_train = sd_train  # start day train
        self.ed_train = sd_test - dt.timedelta(days=1)
        self.sd_test = sd_test  # start day test
        self.ed_test = ed_test  # end day
        self.cd = sd_test  # current day of trading simulation

        self.currency = currency
        self.model = model
        self.tickers = tickers
        self.portvals = []
        self.portdates = []
        self.port = {}
        self.stocks = {}
        for ticker in tickers:
            self.port[ticker] = 0
            self.stocks[ticker] = util.get_data([ticker], pd.date_range(sd_train, ed_test))

    def startSim(self):
        for symbol in self.stocks.keys():
            self.model.addEvidence(symbol, self.stocks[symbol], self.sd_train, self.ed_train)

    def tradeToday(self, trade=True):
        if not trade:
            return 0

        trades = self.model.trade(self.stocks, self.currency, self.port, self.sd_train, self.cd)
        portval = self.currency
        for ticker, numTrades in trades.items():
            stockVal = self.stocks[ticker][self.cd:self.cd][ticker].values[0]
            if stockVal == np.float64('nan'):
                return

            self.port[ticker] += numTrades
            self.currency -= numTrades * stockVal
            if self.port[ticker] < 0:
                raise ValueError('Sold more stocks than you had')

            print(f'{ticker} val on {self.cd} is {stockVal}')

            numStock = self.port[ticker]
            portval += numStock * stockVal

        self.portvals += [portval]
        self.portdates += [self.cd]

    def nextDay(self):
        self.cd += dt.timedelta(days=1)


if __name__ == '__main__':
    sim = Simulation(model=RFLearner())
    sim.startSim()
    print(sim.cd)

    for i in range(5):
        sim.tradeToday()
        sim.nextDay()
        print('Current Day:', sim.cd)
        print('Portfolio:', sim.port)
        print('Value: ', sim.portvals[-1])
        print()

    print(sim.portvals)
    plt.plot(sim.portdates, sim.portvals)
    plt.show()