### Created by Anadi Jaggia
import os

import pandas as pd
import numpy as np
import math
import datetime as dt

import matplotlib.pyplot as plt

from engine import util


def bbands(df_prices, lookback):
    sma = df_prices.rolling(window=lookback, min_periods=lookback).mean()
    stdev = df_prices.rolling(window=lookback, min_periods=lookback).std()

    upper_band = sma + 2 * stdev
    lower_band = sma - 2 * stdev
    # plt.plot(sma)
    # plt.plot(upper_band)
    # plt.plot(lower_band)
    # plt.show()
    return sma + 2 * stdev, sma - 2 * stdev


def momentum(df_prices, lookback):
    df_momentum = pd.DataFrame(np.nan, index=df_prices.index, columns=df_prices.columns.values.tolist())
    df_momentum[lookback:] = (df_prices[lookback:] / df_prices[:-lookback].values) - 1

    # plt.plot(df_momentum)
    return df_momentum


def midpoints(df_prices, lookback):
    df_midpoints = np.mean(df_prices.rolling(window=lookback, min_periods=lookback).max()
                           + df_prices.rolling(window=lookback, min_periods=lookback).min())

    return df_midpoints


def so(price, lookback=14):
    rolling_max = price.rolling(window=lookback, min_periods=lookback).max()
    rolling_min = price.rolling(window=lookback, min_periods=lookback).min()
    daily_range = rolling_max - rolling_min
    so = 100 * ((price - rolling_min) / daily_range)
    # plt.plot(price)
    # plt.plot(so)
    so[so > 80] = 0.02
    so[so < 20] = -0.02
    so[so > 1] = 0.0
    return so


def get_features(df_prices):
    upper_band, lower_band = bbands(df_prices, lookback=20)
    df_momentum = momentum(df_prices, lookback=2)
    df_midpoints = midpoints(df_prices, lookback=85)
    # df_so = so(df_prices)

    df_last_prices = df_prices.shift(1)

    # get percent changes per feature. How else to 'normalize'?
    price_upper = df_prices / upper_band
    price_lower = df_prices / lower_band
    price_midpoint = df_prices / df_midpoints

    # plt.plot(price_midpoint)

    # lastprice_midpoint = df_last_prices / df_midpoints (Did this in class 4 some reason i forget)

    features = pd.concat(
        [
         price_upper,
         price_lower,
         price_midpoint,
         # lastprice_midpoint,
         # df_so,
         df_momentum
         ], axis=1)

    return features


def get_Y(df_returns, YSELL, YBUY):
    def returns_classifier(ret):
        if ret > YBUY:
            return 1.0
        elif ret < YSELL:
            return -1.0
        else:
            return 0.0

    df_Y = df_returns.applymap(returns_classifier)
    return df_Y


def get_features_from_csv(prices, symbols):
    # create data frame
    df_features = pd.DataFrame()
    print(df_features)
    # read from csv
    rootdir = "../indicators_data/"
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            for symbol in symbols:
                full_path = os.path.join(subdir, symbol + ".csv")
                df_temp = pd.read_csv(full_path)
                df_features = pd.concat([df_features, df_temp], axis=1)

    print(df_features)
    return df_features




    # get percent changes per feature. How else to 'normalize'?
    # price_upper = df_prices / upper_band
    # price_lower = df_prices / lower_band
    # price_midpoint = df_prices / df_midpoints

    # plt.plot(price_midpoint)

    # lastprice_midpoint = df_last_prices / df_midpoints (Did this in class 4 some reason i forget)

    # features = pd.concat(
    #     [
    #         price_upper,
    #         price_lower,
    #         price_midpoint,
    #         # lastprice_midpoint,
    #         # df_so,
    #         df_momentum
    #     ], axis=1)

if __name__ == '__main__':
     symbols = ['DIS']
     get_features_from_csv(util.get_data(symbols, pd.date_range(dt.datetime(2018, 1, 1), dt.datetime(2018, 12, 31))), symbols)

