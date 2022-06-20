import yfinance as yf
import pandas as pd

ticker = 'NQ=F'

df = yf.download(tickers=ticker, period="5d", interval='1d')

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

df = df.drop(['Adj Close', 'Volume'], axis=1)
print(df)

df1 = df

frames = [df, df1]
symmetric_df = pd.concat(frames)
print(symmetric_df)
