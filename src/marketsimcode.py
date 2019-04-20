### Created by Anadi Jaggia
import pandas as pd
import numpy as np
from engine import janitor
from engine import util
import matplotlib.pyplot as plt

def get_trans_cost(commission, impact, symbol_price, curr_price, sign):
    if sign == 1:
        return commission + impact*symbol_price*curr_price
    else:
        return commission - impact*symbol_price*curr_price

def get_sd_and_ed(df_trades):
    start_date = df_trades.index.values[0]
    end_date = df_trades.index.values[-1]
    return start_date, end_date


def compute_portvals(df_trades, start_val=100000, commission=0, impact=0):


    syms = df_trades.columns.values.tolist()
    start_date, end_date = get_sd_and_ed(df_trades)
    
    #Reading in price data
    df_prices = util.get_data(syms, pd.date_range(start_date, end_date))
    df_prices = janitor.backfill(df_prices)
    df_prices['Cash'] = np.ones(df_prices.shape[0]) * start_val
    df_prices['NumHeld'] = np.zeros(df_prices.shape[0])
    # print(df_prices)

    #Add cash column and transaction costs
    # df_trades['Cash'] = np.zeros(df_trades.shape[0], )

    prevCash = start_val
    prevHeld = 0
    for index, row in df_trades.iterrows():
        for symbol in syms:
            transaction_costs = 0.0
            # if row[symbol] > 0:
            #     transaction_costs = get_trans_cost(commission, impact, row[symbol], df_prices.loc[index][symbol], 1)
            # elif row[symbol] < 0:
            #     transaction_costs = get_trans_cost(commission, impact, row[symbol], df_prices.loc[index][symbol], -1)
            # else:
            #     transaction_costs = 0.0
            # print(df_prices)
            # print(df_prices['Cash'])
            df_prices['Cash'][index:index] = prevCash + -1*row[symbol]*df_prices.loc[index][symbol] - transaction_costs
            df_prices['NumHeld'][index:index] = prevHeld + row[symbol]
            prevCash = df_prices['Cash'][index:index]
            prevHeld = df_prices['NumHeld'][index:index]
                

    #Building holdings dataframe
    df_holdings = pd.DataFrame(0.0, index=df_prices.index, columns=syms+['Cash'])

    # for date in df_holdings.index:
    #     df_holdings.loc[date] = df_prices[date:date]['Cash'] + \
    #                             df_prices[date:date]['NumHeld'] * df_prices[date:date]['A']
    df_holdings = df_prices['Cash'] + df_prices['NumHeld'] * df_prices[syms[0]]


    #Portfolio values dataframe
    #df_value = df_holdings.multiply(df_prices)

    #Total portfolio value dataframe
    # df_port_val = df_value.sum(axis=1)
    plt.clf()
    df_prices[syms[0]].plot(title=f'{syms[0]} over time')
    return df_holdings

