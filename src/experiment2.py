### Created by Anadi Jaggia ###

import datetime as dt
import numpy as np
import pandas as pd
import StrategyLearner as sl
import marketsimcode as msc
import matplotlib.pyplot as plt

def main():
    # Parameters
    sd_train = dt.datetime(2008, 1, 1)
    ed_train = dt.datetime(2009, 12, 31)
    sym = 'JPM'
    capital = 100000

    impacts = np.linspace(0.0, 0.5, 51)
    num_trades = list()
    bench_cum_ret = list()
    sl_cum_ret = list()

    # Test learner for different market impacts
    for imp in impacts:
        # Train strategy learner
        learner = sl.StrategyLearner(verbose=False, impact=imp)
        learner.addEvidence(symbol=sym, sd=sd_train, ed=ed_train, sv=capital)
        learner.addEvidence()

        # Test strategy learner
        sl_trades = learner.testPolicy(symbol=sym, sd=sd_train, ed=ed_train, sv=capital)
        sl_portvals = msc.compute_portvals(sl_trades, start_val=capital, commission=0.0, impact=imp)

        # Benchmark: Buying 1000 shares of JPM and holding throughout period
        bench_trades = pd.DataFrame(0.0, index=sl_trades.index, columns=[sym])
        bench_trades[sym].iloc[0] = 1000.0
        bench_portvals = msc.compute_portvals(bench_trades, start_val=capital, commission=0.0, impact=imp)

        # Compute cumulative returns
        bench_cum_ret.append(bench_portvals.iloc[-1] / bench_portvals.iloc[0] - 1)
        sl_cum_ret.append(sl_portvals.iloc[-1] / sl_portvals.iloc[0] - 1)

        # Calculate number of trades made by strategy learner
        num_trades.append(len(sl_trades[sl_trades[sym] != 0.0]))

    # Plots
    plt.plot(impacts, num_trades)
    plt.xlabel('Market Impact')
    plt.ylabel('Num. Trades')
    plt.title('Number of Trades vs Market Impact')
    plt.show()

    # plt.plot(impacts, bench_cum_ret, label='Benchmark')
    plt.plot(impacts, sl_cum_ret, label='Strategy Learner')
    plt.legend()
    plt.xlabel('Market Impact')
    plt.ylabel('Cumulative Returns')
    plt.title('Cumulative Return vs Market Impact')
    plt.show()

if __name__ == "__main__":
    main()
