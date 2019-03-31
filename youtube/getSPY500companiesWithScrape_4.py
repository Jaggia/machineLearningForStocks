import time

import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas_datareader.data as web
import pandas as pd
import getData_1

def save_sp500_tickers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies', headers=headers)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]: #1 onwards to skip table headers
        ticker = row.findAll('td')[1].text
        ticker = ticker.encode('ascii', 'ignore')
        if '.' not in ticker:
            tickers.append(ticker)

    if not os.path.exists('data'):
        os.makedirs('data')
    with open("data/sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers

def get_data_from_interwebs(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("data/sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    start = '01-01-2014'
    end = '22-03-2019'
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('data/{}.csv'.format(ticker)):
            print ticker
            try:
                df = getData_1.download_data([ticker], internal=False, start=start, end=end)
            except AssertionError:
                print("assertion error")
                time.sleep(5)
                get_data_from_interwebs()
            # print(df)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df = df.drop("index", axis=1)
            df.to_csv('data/{}.csv'.format(ticker))
            # time.sleep(2)
        else:
            print('Already have {}'.format(ticker))


def compile_data():
    with open("data/sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('data/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'index'], axis=1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_adj_closes.csv')


if __name__ == "__main__":
    # save_sp500_tickers()
    # get_data_from_interwebs()
    compile_data()