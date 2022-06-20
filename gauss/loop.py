import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

ticker = 'NQ=F'

df = yf.download(tickers=ticker, period="5d", interval='1d')

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

df = df.drop(['Adj Close', 'Volume'], axis=1)
print(df)

df_start_high = df['High'].iloc[0]  # get first row of selection
df_end_high = df['High'].iloc[-1]  # get last row of selection

diff = df_start_high - df_end_high
print(diff)

selection_df = df - diff
print(selection_df)

frames = [df, selection_df]
symmetric_df = pd.concat(frames)
print(symmetric_df)

symmetric_df = symmetric_df.reset_index(drop=True)

# next loop

df_start_high = selection_df['High'].iloc[0]  # get first row of selection
df_end_high = selection_df['High'].iloc[-1]  # get last row of selection

diff = df_start_high - df_end_high
print(diff)

selection_df = selection_df - diff
print(selection_df)

frames = [symmetric_df, selection_df]
symmetric_df = pd.concat(frames)
print(symmetric_df)

symmetric_df = symmetric_df.reset_index(drop=True)

print(symmetric_df)

# next loop

df_start_high = selection_df['High'].iloc[0]  # get first row of selection
df_end_high = selection_df['High'].iloc[-1]  # get last row of selection

diff = df_start_high - df_end_high
print(diff)

selection_df = selection_df - diff
print(selection_df)

frames = [symmetric_df, selection_df]
symmetric_df = pd.concat(frames)
print(symmetric_df)

symmetric_df = symmetric_df.reset_index(drop=True)

print(symmetric_df)

fig = go.Figure(data=[go.Candlestick(x=symmetric_df.index,
                                      open=symmetric_df['Open'],
                                      high=symmetric_df['High'],
                                      low=symmetric_df['Low'],
                                      close=symmetric_df['Close'])])

fig.update_layout(
    hovermode='x unified',
    title=ticker,
    showlegend=False,
    width=1800,
    height=800,
    xaxis_rangeslider_visible=False)

fig.write_html('output_file_name.html', auto_open=True )
