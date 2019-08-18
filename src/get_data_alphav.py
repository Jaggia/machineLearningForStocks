import pandas as pd
from time import mktime
import datetime

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from sys import platform as sys_pf
from pprint import pprint
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

def convert_to_unix(date):
    """
    converts date to unix timestamp

    parameters: date - in format (dd-mm-yyyy)

    returns integer unix timestamp
    """
    datum = datetime.strptime(date, '%d-%m-%Y')

    return int(mktime(datum.timetuple()))


def getPrices(stocks, plot=False, write_to_csv=False):
    for stock in stocks:
        ts = TimeSeries(key='UOVDY8C1SRAQHY5D', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=stock, interval='1min', outputsize='full')
        # data, meta_data = ts.get_daily(symbol='DIS', outputsize='full')

        pprint(meta_data)

        if plot:
            data['4. close'].plot()
            plt.title('Prices for the' + stock + 'stock (1 min)')
            plt.xticks(rotation=15)  # Help prevent axis labels from overlapping
            plt.show()

        if write_to_csv:
            csv_data = pd.DataFrame(data)
            csv_data.to_csv("../prices_data/" + stock + "/full.csv", index=False)


def getIndicators(stocks, plot=False, write_to_csv=False):
    for stock in stocks:
        ti = TechIndicators(key='UOVDY8C1SRAQHY5D', output_format='pandas')
        data, meta_data = ti.get_ema(symbol=stock, interval='60min', time_period=20)

        pprint(meta_data)

        if plot:
            data.plot()
            plt.title('Ema Indicator for the ' + stock + ' stock (60 min)')
            plt.xticks(rotation=15)  # Help prevent axis labels from overlapping
            plt.show()

        if write_to_csv:
            csv_data = pd.DataFrame(data)
            csv_data.to_csv("../indicators_data/EMA/" + stock + ".csv", index=False)


if __name__ == "__main__":
    stocks = ['IBM', 'GOOG', 'AAPL', 'SPY', 'MJ']
    # stocks = ['XLF']
    cols = []

    # getPrices(stocks, plot=True, write_to_csv=False)
    getIndicators(stocks, plot=True, write_to_csv=False)


