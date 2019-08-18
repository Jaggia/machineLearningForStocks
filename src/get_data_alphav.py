# DJN - DEAD CODE
# import requests                  # [handles the http interactions](http://docs.python-requests.org/en/master/)
# from bs4 import BeautifulSoup    # beautiful soup handles the html to text conversion and more
# import re                        # regular expressions are necessary for finding the crumb (more on crumbs later)
# from datetime import datetime    # string to datetime object conversion
# from time import mktime          # mktime transforms datetime objects to unix timestamps

# def _get_crumbs_and_cookies(stock):
#     """
#     get crumb and cookies for historical data csv download from yahoo finance
#
#     parameters: stock - short-handle identifier of the company
#
#     returns a tuple of header, crumb and cookie
#     """
#
#     url = 'https://finance.yahoo.com/quote/{}/history'.format(stock)
#     with requests.session():
#         header = {'Connection': 'keep-alive',
#                   'Expires': '-1',
#                   'Upgrade-Insecure-Requests': '1',
#                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
#                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
#                   }
#
#         website = requests.get(url, headers=header)
#         soup = BeautifulSoup(website.text, 'lxml')
#         crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))
#
#         return (header, crumb[0], website.cookies)
import os
import pandas as pd
from time import mktime
import datetime

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from sys import platform as sys_pf
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


# def load_csv_data(stock, interval='1d', day_begin='01-03-2018', day_end='22-03-2019'):
#     """
#     queries yahoo finance api to receive historical data in csv file format
#
#     parameters:
#         stock - short-handle identifier of the company
#
#         interval - 1d, 1wk, 1mo - daily, weekly monthly data
#
#         day_begin - starting date for the historical data (format: dd-mm-yyyy)
#
#         day_end - final date of the data (format: dd-mm-yyyy)
#
#     returns a list of comma seperated value lines
#     """
#     day_begin_unix = convert_to_unix(day_begin)
#     day_end_unix = convert_to_unix(day_end)
#
#     header, crumb, cookies = _get_crumbs_and_cookies(stock)
#
#     with requests.session():
#         url = 'https://query1.finance.yahoo.com/v7/finance/download/' \
#               '{stock}?period1={day_begin}&period2={day_end}&interval={interval}&events=history&crumb={crumb}' \
#             .format(stock=stock, day_begin=day_begin_unix, day_end=day_end_unix, interval=interval, crumb=crumb)
#
#         website = requests.get(url, headers=header, cookies=cookies)
#
#         return website.text.split('\n')[:-1]


def getPrices(stocks):
    for stock in stocks:
        ts = TimeSeries(key='UOVDY8C1SRAQHY5D', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=stock, interval='1min', outputsize='full')
        # data, meta_data = ts.get_daily(symbol='DIS', outputsize='full')
        data['4. close'].plot()
        # plt.title('Intraday Times Series for the MSFT stock (1 min)')
        plt.title('Daily Times Series for the ', stock, ' stock (1 min)')
        plt.show()

def getIndicators(stocks):
    for stock in stocks:
        ti = TechIndicators(key='UOVDY8C1SRAQHY5D', output_format='pandas')
        data, meta_data = ti.get_ema(symbol=stock, interval='60min', time_period=20)
        # data.plot()
        # plt.title(('ema indicator for ', stock, ' stock (60 min)'))
        # plt.show()
        csvData = pd.DataFrame(data)
        csvData.to_csv("../indicators_data/EMA/" + stock + ".csv", index=False)


if __name__ == "__main__":
    # stocks = ['IBM', 'GOOG', 'AAPL', 'SPY', 'MJ']
    stocks = ['XLF']
    cols = []

    # DEAD CODE - DJN
    # for stock in stocks:
    #     csvData = load_csv_data(stock)
    #     csvData = [item.split(',') for item in csvData]
    #     cols = csvData[0]
    #     csvData = pd.DataFrame(csvData[1:], columns=cols)
    #     csvData.to_csv("../indicators_data/newStocks/" + stock + ".csv", index=False)

    # getPrices(stocks)
    getIndicators(stocks)


