import os
import pandas as pd

from colorama import Fore, Style
LOG_COLOR = Style.BRIGHT + Fore.GREEN
ERR_COLOR = Style.BRIGHT + Fore.RED
print(LOG_COLOR + 'using this color for logs')

#Get CSV file path for stock symbol
def symbol_to_path(symbol, base_dir=None):
    if base_dir is None:
        base_dir = os.environ.get("MARKET_DATA_DIR", '../data/')
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


#Read stock data for given symbols from CSV files
def get_data(symbols, date_range, addSPY=False, colname = 'Adj Close'):
    df = pd.DataFrame(index=date_range)
    if addSPY and 'SPY' not in symbols:
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv('../data/{}.csv'.format(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', colname], na_values=['nan'])
        df_temp = df_temp.rename(columns={colname: symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':
            df = df.dropna(subset=["SPY"])

    return df


#Plot time series of stock prices
def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    import matplotlib.pyplot as plt
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
