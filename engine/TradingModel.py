import numpy as np
from colorama import Fore, Style
LOG_COLOR = Style.BRIGHT + Fore.GREEN
ERR_COLOR = Style.BRIGHT + Fore.RED
print(LOG_COLOR + 'using this color for logs')

class TradingModel(object):
    def addEvidence(self, symbol, data, sd, ed):
        pass

    def trade(self, symbol, data, cd, currency, port):
        # buy or sell given historic info for stock
        # pastInfo : dict {str, list}, past stocks values
        # currency : int, amount of currency availabl
        # stocks : dict {str, int}, amount of each stock owned

        print(ERR_COLOR + 'USING NAIVE TRADING MODEL' + LOG_COLOR)
        if port > 0:
            # either sell 1 stock, do nothing, buy 1 stock
            trades = np.random.randint(-1, 2)
        else:
            # either buy 1 stock or do nothin
            trades = np.random.randint(0, 2)

        return trades