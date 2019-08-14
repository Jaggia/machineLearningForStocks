import os

# DJN - DEAD CODE
# import requests                  # [handles the http interactions](http://docs.python-requests.org/en/master/)
# from bs4 import BeautifulSoup    # beautiful soup handles the html to text conversion and more
# import re                        # regular expressions are necessary for finding the crumb (more on crumbs later)
from datetime import datetime      # string to datetime object conversion
from time import mktime            # mktime transforms datetime objects to unix timestamps

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

def convert_to_unix(date):
    """
    converts date to unix timestamp

    parameters: date - in format (dd-mm-yyyy)

    returns integer unix timestamp
    """
    datum = datetime.strptime(date, '%d-%m-%Y')

    return int(mktime(datum.timetuple()))

if __name__ == "__main__":
    stocks = ['IBM', 'GOOG', 'AAPL', 'SPY', 'MJ']
    # stocks = ['XLF']
    cols = []

    # DEAD CODE - DJN
    # for stock in stocks:
    #     csvData = load_csv_data(stock)
    #     csvData = [item.split(',') for item in csvData]
    #     cols = csvData[0]
    #     csvData = pd.DataFrame(csvData[1:], columns=cols)
    #     csvData.to_csv("../data/newStocks/" + stock + ".csv", index=False)

    for stock in stocks:
        ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=stock, interval='1min', outputsize='full')
        data['4. close'].plot()
        plt.title('Intraday Times Series for the {} stock (1 min)'.format(stock))
        plt.xticks(rotation=75)
        plt.show()

