import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# https://www.opentechguides.com/how-to/article/pandas/193/index-slice-subset.html

ticker = 'NQ=F'

# forward df
df = yf.download(tickers=ticker, period='3mo', interval='1d')
df.reset_index(inplace=True)
print(df)
last_row = df.index[-1]
print(last_row)

