import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import numpy as np
from finta import TA
from datetime import timedelta

# ticker = yf.Ticker(symbol)

ticker = "NQ=F"

# data = yf.download(tickers = ticker, start='2019-01-04', end='2021-06-09')
data = yf.download(tickers=ticker, period="6mo", interval='1d')

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

df1 = pd.DataFrame(data)

df = df1.reset_index()

df7 = df.rename(
    columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'},
    inplace=False)

df7.to_csv('daily.csv')

n = 1

df3 = df7.groupby(np.arange(len(df7)) // n).max()
# print('df3 max:', df3)

df4 = df7.groupby(np.arange(len(df7)) // n).min()
# print('df4 min:', df4)

df5 = df7.groupby(np.arange(len(df7)) // n).first()
# print('df5 open:', df5)

df6 = df7.groupby(np.arange(len(df7)) // n).last()
# print('df6 close:', df6)

agg_df = pd.DataFrame()

agg_df['date'] = df6['date']
agg_df['low'] = df4['low']
agg_df['high'] = df3['high']
agg_df['open'] = df5['open']
agg_df['close'] = df6['close']

# print(agg_df)

df2 = agg_df

# print(df2)
num_periods = 21
df2['SMA'] = TA.SMA(df2, 21)
df2['FRAMA'] = TA.FRAMA(df2, 10)
df2['WMA'] = TA.WMA(df2, 9)
df2['TEMA'] = TA.TEMA(df2, num_periods)
# df2['VWAP'] = TA.VWAP(df2)

# ATR

num_periods_ATR = 21
multiplier = 1

df2['ATR_diff'] = df2['high'] - df2['low']
df2['ATR'] = df2['ATR_diff'].ewm(span=num_periods_ATR, adjust=False).mean()
df2['Line'] = df2['WMA'].round(2)
df2['line_change'] = df2['Line'] / df2['Line'].shift(1)
df3 = pd.DataFrame()
df3['date'] = df2['date']
df3['close'] = df2['line_change']
df3['open'] = df2['line_change']
df3['high'] = df2['line_change']
df3['low'] = df2['line_change']

# calculate projection angle
periods_change = 8  # drives the projection

df3['change_SMA'] = TA.WMA(df3, periods_change)  # drives the projection
df2['change_SMA'] = df3['change_SMA']

df2['upper_band'] = df2['Line'] + multiplier * df2['ATR']
df2['lower_band'] = df2['Line'] - multiplier * df2['ATR']

multiplier_1 = 1.6
multiplier_2 = 2.3

df2['upper_band_1'] = (df2['Line'] + multiplier_1 * df2['ATR']).round(2)
df2['lower_band_1'] = (df2['Line'] - multiplier_1 * df2['ATR']).round(2)

df2['upper_band_2'] = df2['Line'] + multiplier_2 * df2['ATR'].round(2)
df2['lower_band_2'] = df2['Line'] - multiplier_2 * df2['ATR'].round(2)

fig1 = go.Figure(data=[go.Candlestick(x=df2['date'],
                                      open=df2['open'],
                                      high=df2['high'],
                                      low=df2['low'],
                                      close=df2['close'])]

                 )

fig1.add_trace(
    go.Scatter(
        x=df2['date'],
        y=df2['upper_band'].round(2),
        name='upper band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=df2['date'],
        y=df2['lower_band'].round(2),
        name='lower band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=df2['date'],
        y=df2['upper_band_1'].round(2),
        name='upper band_1',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=df2['date'],
        y=df2['lower_band_1'].round(2),
        name='lower band_1',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=df2['date'],
        y=df2['Line'],
        name="WMA",
        mode="lines",
        line=go.scatter.Line(color="blue"),
        )
)

fig1.update_layout(
    hovermode='x unified',
    title=ticker,
    showlegend=False,
    width=1800,
    height=800,
    xaxis_rangeslider_visible=False
)

fig1.write_html( 'output_file_name.html',
                   auto_open=True )