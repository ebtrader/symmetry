import yfinance as yf
import plotly.graph_objects as go
from scipy.signal import argrelextrema
import numpy as np

# https://raposa.trade/blog/higher-highs-lower-lows-and-calculating-price-trends-in-python/

# https://plotly.com/python/marker-style/

ticker = 'NQ=F'

df = yf.download(tickers=ticker, period='6mo', interval='1d')
#df = yf.download(tickers = ticker, start='2013-01-01', end='2014-12-31')

df = df.reset_index()

fig1 = go.Figure(data=[go.Candlestick(x=df['Date'],
                                      open=df['Open'],
                                      high=df['High'],
                                      low=df['Low'],
                                      close=df['Close'], showlegend=False)])

fig1.write_html( 'output_file_name.html',
                   auto_open=True )

