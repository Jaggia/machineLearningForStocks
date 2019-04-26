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
                 currency=10000,
                 model=RFLearner(),
                 tickers= ("AIG", "ABT")):  # 'MSFT', 'AMZN', 'IBM', 'AAPL')):

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
        self.correct = {True: 0, False: 0}
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

        portval = 0
        for ticker, numTrades in trades.items():
            numTrades = numTrades[-1]
            stockVals = self.stocks[ticker][self.cd:self.cd][ticker]
            if len(stockVals) == 0:
                return 0
            stockVal = stockVals.values[0]
            if str(stockVal) == 'nan':
                return 0

            try:
                # log how often model is correct
                increase = self.stocks[ticker][self.cd:self.cd].values[0] < \
                         self.stocks[ticker][self.cd+dt.timedelta(days=1):
                                             self.cd+dt.timedelta(days=1)].values[0]
                correct = (increase and trades[ticker][-1] > 0) or (not increase and trades[ticker][-1] <= 0)
                self.correct[correct] += 1
                # print(self.correct)
            except:
                pass

            self.port[ticker] += numTrades
            self.currency -= numTrades * stockVal
            # if self.port[ticker] < 0:
            #     raise ValueError(util.ERR_COLOR + 'Sold more stocks than you had')

            # print('{} val on {} is {}'.format(ticker, self.cd, stockVal))

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

    for i in range(100):
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
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')
    plt.title('Portfolio Value over time')
    plt.show()