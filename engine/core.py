import engine.util as util
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

from engine import janitor
from engine.RandomForest import RFLearner


class Simulation(object):
    def __init__(self,
                 sd_train=dt.datetime(2018, 1, 1),
                 ed_train=dt.datetime(2018, 12, 31),
                 sd_test=dt.datetime(2019, 1, 1),
                 ed_test=dt.datetime(2019, 3, 22),
                 currency=1000000,
                 model=RFLearner(),
                 tickers= "A"):  # 'MSFT', 'AMZN', 'IBM', 'AAPL')):

        self.sd_train = sd_train  # start day train
        # self.ed_train = sd_test - dt.timedelta(days=1)
        self.ed_train = ed_train
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
        for symbol in self.tickers:
            self.stocks[symbol] = janitor.backfill(self.stocks[symbol])
            self.model.addEvidence(symbol, self.stocks[symbol], self.sd_train, self.ed_train)


    def tradeToday(self, trade=True, retrain=False):
        if not trade:
            return 0

        if retrain:
            for symbol in self.tickers:
                self.model.addEvidence(symbol, self.stocks[symbol],
                                       self.sd_train, self.cd)

        trades = {}
        for ticker in self.tickers:
            trades[ticker] = self.model.testAndBuildTradingDecisions(ticker, self.stocks[ticker],
                                                                     self.sd_train, self.cd,
                                                                     visualize=True)
            # print('TRADES' + str(trades[ticker]))

        portval = 0
        for ticker, numTrades in trades.items():
            numTrades = numTrades[-1]
            stockVal = self.stocks[ticker][self.cd:self.cd][ticker].values[0]
            if str(stockVal) == 'nan':
                return 0

            self.port[ticker] += numTrades
            self.currency -= numTrades * stockVal
            # if self.port[ticker] < 0:
            #     raise ValueError(util.ERR_COLOR + 'Sold more stocks than you had')

            print('{} val on {} is {}'.format(ticker, self.cd, stockVal))

            numStock = self.port[ticker]
            portval += numStock * stockVal

        portval += self.currency
        self.portvals += [portval]
        self.portdates += [self.cd]

    def nextDay(self):
        self.cd += dt.timedelta(days=1)


if __name__ == '__main__':
    sim = Simulation(model=RFLearner())
    sim.startSim()
    print(sim.cd)

    for i in range(365):
        sim.tradeToday(retrain=False)
        sim.nextDay()
        # print('Current Day:', sim.cd)
        # print('Portfolio:', sim.port)
        # print('Currency:', sim.currency)
        # try:
            # fails if no portfolio yet (market closed at start of sim)
            # print('Value: ', sim.portvals[-1])
        # except:
        #     pass
        # print()

    # print(sim.portvals)
    f, ax = plt.subplots(1)
    #ax.plot(sim.portdates, sim.portvals)
    ax.plot(sim.portdates, sim.portvals)
    plt.show()