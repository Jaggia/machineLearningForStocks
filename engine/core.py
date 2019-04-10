from code import util
from code.StrategyLearner import StrategyLearner
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

from colorama import Fore, Style
LOG_COLOR = Style.BRIGHT + Fore.GREEN
ERR_COLOR = Style.BRIGHT + Fore.RED
print(LOG_COLOR + 'using this color for logs')


class TradingModel(object):
    def trade(self, pastInfo, currency, port, sd, ed):
        # buy or sell given historic info for stock
        # pastInfo : dict {str, list}, past stocks values
        # currency : int, amount of currency availabl
        # stocks : dict {str, int}, amount of each stock owned

        print(ERR_COLOR + 'USING NAIVE TRADING MODEL' + LOG_COLOR)
        trades = {}
        for ticker in port.keys():
            if port[ticker] > 0:
                # either sell 1 stock, do nothing, buy 1 stock
                trades[ticker] = np.random.randint(-1, 2)
            else:
                # either buy 1 stock or do nothin
                trades[ticker] = np.random.randint(0, 2)

        return trades

class NStrategyLearner(TradingModel):
    def __init__(self):
        self.tickers = []
        self.learners = {}

    def addEvidence(self, symbol, sd, ed):
        print('Adding evidence', symbol, sd, ed)
        self.learners[symbol] = StrategyLearner()
        self.learners[symbol].addEvidence(symbol, sd, ed)

    def trade(self, pastInfo, currency, port, sd, ed):
        trades = {}
        for symbol in port.keys():
            #print('trading', symbol, sd, ed)
            self.addEvidence(symbol, sd, ed)
            symTrades = self.learners[symbol].testPolicy(symbol, sd, ed)
            #print('STRAT TRADES', trades)
            trades[symbol] = np.round(symTrades[-1][0])
            if port[symbol] <= -trades[symbol]:  # if trying to sell more than you have
                trades[symbol] = -port[symbol]  # just sell everything

        print(f'Trades on {ed} are {trades}')
        return trades



class Simulation(object):
    def __init__(self,
                 sd=dt.datetime(2008, 1, 1),
                 ed=dt.datetime(2010, 11, 1),
                 currency=10000,
                 model=TradingModel(),
                 tickers=('GOOG', 'MSFT',)):# 'AMZN', 'IBM', 'AAPL')):
        self.sd = sd  # start day
        self.cd = sd  # curr day of simulation
        self.ed = ed  # end day
        self.currency = currency
        self.model = model
        self.tickers = tickers
        self.portvals = []
        self.portdates = []
        self.port = {}
        self.stocks = {}
        for ticker in tickers:
            self.port[ticker] = 0
            self.stocks[ticker] = util.get_data([ticker], dates=(sd, ed))

    def startSim(self):
        pass

    def nextDay(self, trade=True):
        if not trade:
            self.cd += dt.timedelta(days=1)
            return 0

        pastInfo = self.tickers
        trades = self.model.trade(pastInfo, self.currency, self.port, self.sd, self.cd)
        for ticker, numTrades in trades.items():
            stockVals = util.get_data([ticker], (self.cd, self.cd))
            stockVal = -1
            for index, row in stockVals.iterrows():
                #print(f'Stockvals index {index} row {row}')
                stockVal = row[ticker]

            if stockVal == -1:
                self.cd += dt.timedelta(days=1)
                return  # market closed
                raise ValueError(f"Can't find stockVal for {ticker} on {self.cd}\n{stockVals}")

            self.port[ticker] += numTrades
            print(stockVal)
            self.currency -= numTrades * stockVal
            if self.port[ticker] < 0:
                raise ValueError('Sold more stocks than you had')

        portval = self.currency
        for ticker, numStock in self.port.items():
            stockVals = util.get_data([ticker], (self.cd, self.cd))
            stockVal = -1
            for index, row in stockVals.iterrows():
                #print(f'Stockvals index {index} row {row}')
                stockVal = row[ticker]

            if stockVal == -1:
                raise ValueError(f"Can't find stockVal for {ticker} on {self.cd}")

            print(f'{ticker} val on {self.cd} is {stockVal}')
            portval += numStock * stockVal
        self.portvals += [portval]
        self.portdates += [self.cd]

        self.cd += dt.timedelta(days=1)
        return


if __name__ == '__main__':
    sim = Simulation(model=NStrategyLearner())
    sim.startSim()
    print(sim.cd)
    for i in range(1000):
        # have to advance days so model has something to train on
        sim.nextDay(trade=False)
        #print('Current Day:', sim.cd)
        #print('Portfolio:', sim.port)
        #print()

    for i in range(5):
        sim.nextDay()
        print('Current Day:', sim.cd)
        print('Portfolio:', sim.port)
        print('Value: ', sim.portvals[-1])
        print()

    print(sim.portvals)
    plt.plot(sim.portdates, sim.portvals)
    plt.show()