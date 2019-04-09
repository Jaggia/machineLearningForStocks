import numpy as np

class tradingModel(object):
    def buyOrSell(self, pastInfo):
        # buy or sell given historic info for stock
        # randomly return -1 or 1 for selling 1 or buying 1 stock
        return int(np.random.randint(0, 2) * 2 - 1)

class Core(object):
    def __init__(self, sd='2008-01-01',
                 ed='present',
                 model=tradingModel(),
                 availTickers=['GOOGL', 'MSFT', 'AMZN', 'FB', 'IBM', 'AAPL']):
        self.sd = sd
        self.ed = ed
        self.model = model
        self.availTickers = availTickers


if __name__ == '__main__':
    model = tradingModel()
    for i in range(100):
        print(model.buyOrSell([1, 2, 3]))