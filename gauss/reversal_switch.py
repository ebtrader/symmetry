import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import numpy as np
from finta import TA
import math
from datetime import timedelta

reversal = 0

START = 80
END = 95

# ticker = yf.Ticker(symbol)

ticker = "NQ=F"

# data = yf.download(tickers = ticker, start='2019-01-04', end='2021-06-09')
data = yf.download(tickers=ticker, period="6mo", interval='1d')

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

df1 = pd.DataFrame(data)

df = df1.reset_index()

last_row = df.index[-1] + 0.5

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

# Gauss
num_periods_gauss = 15.5
df2['symbol'] = 2 * math.pi / num_periods_gauss
df2['beta'] = (1 - np.cos(df2['symbol'])) / ((1.414) ** (0.5) - 1)
df2['alpha'] = - df2['beta'] + (df2['beta'] ** 2 + df2['beta'] * 2) ** 2

# Gauss equation
# initialize
df2.loc[0, 'gauss'] = df2.loc[0, 'close']
df2.loc[1, 'gauss'] = df2.loc[1, 'close']
df2.loc[2, 'gauss'] = df2.loc[2, 'close']
df2.loc[3, 'gauss'] = df2.loc[3, 'close']
df2.loc[4, 'gauss'] = df2.loc[4, 'close']

for i in range(4, len(df2)):
    df2.loc[i, 'gauss'] = df2.loc[i, 'close'] * df2.loc[i, 'alpha'] ** 4 + (4 * (1 - df2.loc[i, 'alpha'])) * \
                          df2.loc[i - 1, 'gauss'] \
                          - (6 * ((1 - df2.loc[i, 'alpha']) ** 2) * df2.loc[i - 2, 'gauss']) \
                          + (4 * (1 - df2.loc[i, 'alpha']) ** 3) * df2.loc[i - 3, 'gauss'] \
                          - ((1 - df2.loc[i, 'alpha']) ** 4) * df2.loc[i - 4, 'gauss']


# ATR

num_periods_ATR = 21
multiplier = 1

df2['ATR_diff'] = df2['high'] - df2['low']
df2['ATR'] = df2['ATR_diff'].ewm(span=num_periods_ATR, adjust=False).mean()
# df2['Line'] = df2['WMA'].round(2)
df2['Line'] = df2['gauss']
df2['line_change'] = df2['Line'] / df2['Line'].shift(1)

df2['upper_band'] = df2['Line'] + multiplier * df2['ATR']
df2['lower_band'] = df2['Line'] - multiplier * df2['ATR']

multiplier_1 = 1.6
multiplier_2 = 2.3

df2['upper_band_1'] = (df2['Line'] + multiplier_1 * df2['ATR']).round(2)
df2['lower_band_1'] = (df2['Line'] - multiplier_1 * df2['ATR']).round(2)

df2['upper_band_2'] = df2['Line'] + multiplier_2 * df2['ATR'].round(2)
df2['lower_band_2'] = df2['Line'] - multiplier_2 * df2['ATR'].round(2)

# df2.reset_index(drop=True)

print(df2)

select3 = df2[df2.index.isin({START})]  # Choose by index
select4 = df2[df2.index.isin({END})]  # Choose by index

idx1 = select3.index.item()
idx2 = select4.index.item()

selection_df = df2.loc[idx1:idx2]

print(selection_df)

y0 = max(selection_df['high'])
y1 = min(selection_df['low'])

x0 = selection_df.index[0] - 0.5
x1 = selection_df.index[-1] + 0.5
length_of_selection = x1 - x0

selection_df = selection_df.reset_index(drop=True)
selection_df = selection_df.drop('date', 1)
last_row_select = selection_df.index[-1] + 2

# calculate diff
# take difference between 'high' of first df first row and second df last row
df_high = df2['high'].iloc[-1]        # get last row of our starting point

if reversal == 1:
    selection_df_high = selection_df['high'].iloc[-1]       # get last row of selection for reversal
else:
    selection_df_high = selection_df['high'].iloc[0]       # get first row of selection

diff = selection_df_high - df_high
print(diff)

selection_df -= diff

# # USE FOR REVERSAL
if reversal == 1:
    selection_df = selection_df.iloc[::-1]

frames = [df2, selection_df]
symmetric_df = pd.concat(frames)

symmetric_df = symmetric_df.reset_index(drop=True)

symmetric_df = symmetric_df.reset_index(drop=True)

# print(symmetric_df)
forecast_df = symmetric_df.tail(last_row_select)
# print(forecast_df)

fig1 = go.Figure(data=[go.Candlestick(x=df2.index,
                                      open=df2['open'],
                                      high=df2['high'],
                                      low=df2['low'],
                                      close=df2['close'])]

                 )

fig1.add_trace(go.Candlestick(x=forecast_df.index,
                                      open=forecast_df['open'],
                                      high=forecast_df['high'],
                                      low=forecast_df['low'],
                                      close=forecast_df['close'])

                 )

fig1.add_trace(
    go.Scatter(
        x=df2.index,
        y=df2['upper_band'].round(2),
        name='upper band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=df2.index,
        y=df2['lower_band'].round(2),
        name='lower band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=forecast_df.index,
        y=forecast_df['upper_band'].round(2),
        name='upper band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=forecast_df.index,
        y=forecast_df['lower_band'].round(2),
        name='lower band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)


fig1.add_trace(
    go.Scatter(
        x=df2.index,
        y=df2['upper_band_1'].round(2),
        name='upper band_1',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=df2.index,
        y=df2['lower_band_1'].round(2),
        name='lower band_1',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=forecast_df.index,
        y=forecast_df['upper_band_1'].round(2),
        name='upper band_1',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=forecast_df.index,
        y=forecast_df['lower_band_1'].round(2),
        name='lower band_1',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=df2.index,
        y=df2['Line'],
        name="gauss",
        mode="lines",
        line=go.scatter.Line(color="blue"),
        )
)

fig1.add_trace(
    go.Scatter(
        x=forecast_df.index,
        y=forecast_df['Line'],
        name="gauss",
        mode="lines",
        line=go.scatter.Line(color="blue"),
        )
)

fig1.add_shape(type="rect",
    x0=x0, y0=y0, x1=x1, y1=y1,
    line=dict(color="RoyalBlue"),)

fig1.update_layout(
    hovermode='x unified',
    title=ticker,
    showlegend=False,
    width=1800,
    height=800,
    xaxis_rangeslider_visible=False
)

fig1.add_vline(x=last_row, line_width=3, line_dash="dash", line_color="green")

text_spacer = 6

fig1.add_annotation(text='Actuals', x=last_row - text_spacer, y=15000, showarrow=False, font_size=20)

fig1.add_annotation(text='Forecast', x=last_row + text_spacer, y=15000, showarrow=False, font_size=20)

fig1.write_html( 'output_file_name.html',
                   auto_open=True )

