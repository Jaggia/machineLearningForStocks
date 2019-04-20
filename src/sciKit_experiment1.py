### Created by Anadi Jaggia
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import pandas as pd
import datetime as dt
from src import StrategyLearner as sl
from matplotlib import style
from src import marketsimcode as msc
import matplotlib.pyplot as plt
style.use('ggplot')

def plot_me(sl_port_vals, benchwarmer_port_vals):
    sl_port_vals_norm = sl_port_vals / sl_port_vals.iloc[0]
    benchwarmer_port_vals_norm = benchwarmer_port_vals / benchwarmer_port_vals.iloc[0]
    df_compare = pd.DataFrame({'Strategy Learner': sl_port_vals_norm.values,
                               'Benchmark': benchwarmer_port_vals_norm.values},
                              index=sl_port_vals_norm.index)
    return df_compare


def main():

    # Parameters
    sd_train = dt.datetime(2014, 1, 1)
    ed_train = dt.datetime(2017, 12, 31)
    sd_test = dt.datetime(2018, 1, 1)
    ed_test = dt.datetime(2018, 3, 31)
    sym = 'V'
    capital = 100000

    # Time to train for the big match
    learner = sl.StrategyLearner()
    learner.addEvidence(symbol=sym, sd=sd_train,
                        ed=ed_train, sv=capital)

    # Test your strat learner
    sl_trades = learner.testPolicy(symbol=sym,
                                   sd=sd_test,
                                   ed=ed_test,
                                   sv=capital)
    sl_port_vals = msc.compute_portvals(sl_trades, start_val=capital,
                                        commission=0.0, impact=0.0)

    benchmark_stock = 'SPY'
    # Benchmark of buying a 1000 and HODLing
    benchwarmer_trades = pd.DataFrame(0.0, index=sl_trades.index, columns=[benchmark_stock])
    benchwarmer_trades[benchmark_stock].iloc[0] = 1000.0
    benchwarmer_port_vals = msc.compute_portvals(benchwarmer_trades, start_val=capital,
                                            commission=0.0, impact=0.0)


    # Finally Plot it
    df_plotting = plot_me(sl_port_vals, benchwarmer_port_vals)
    # ax = df_plotting.plot(title='Comparing Strategies - In of Sample Period', fontsize=12)
    # ax = df_plotting.plot(title='Comparing Strategies - Out of Sample Period', fontsize=12)
    ax = df_plotting.plot(title='benchwarmer and port', fontsize=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    plt.show()


if __name__ == "__main__":
    main()

