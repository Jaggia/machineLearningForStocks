from code import util
from code.StrategyLearner import StrategyLearner
from engine.core import TradingModel
import numpy as np
import datetime as dt

from colorama import Fore, Style
LOG_COLOR = Style.BRIGHT + Fore.GREEN
ERR_COLOR = Style.BRIGHT + Fore.RED
print(LOG_COLOR + 'using this color for logs')


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
