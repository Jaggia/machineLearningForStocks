import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mpl_finance as mplf
import matplotlib.dates as mdates
import pandas as pd

df = pd.read_csv('data/TSLA.csv', parse_dates=True, index_col=0)

df_resample_with_ohlc = df['Adj Close'].resample('10D').ohlc()
df_resample_with_volume = df['Volume'].resample('10D').sum()

df_resample_with_ohlc.reset_index(inplace=True)
#convert datetime object to mdate cuz candlestick needs mdates instead of datetime object
df_resample_with_ohlc['Date'] = df_resample_with_ohlc['Date'].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex = ax1)
ax1.xaxis_date()


mplf.candlestick_ohlc(ax1, df_resample_with_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_resample_with_volume.index.map(mdates.date2num), df_resample_with_volume.values, 0)

plt.show()