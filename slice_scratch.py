import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# https://www.opentechguides.com/how-to/article/pandas/193/index-slice-subset.html

ticker = 'NQ=F'

# forward df
df = yf.download(tickers=ticker, period='3mo', interval='1d')
print(df)

df = df.reset_index()

# df = df.reset_index(drop=True)

# selection_df = df.loc[1:5]

# select = df[df['Low'].isin({14293.5})]  # Choose by a price
select = df[df['Date'].isin({'2022-06-13'})]  # Choose by date

# Choose between 2 dates
select1 = df[df['Date'].isin({'2022-03-23'})]  # Choose by date
select2 = df[df['Date'].isin({'2022-06-13'})]  # Choose by date

print(select)

idx1 = select1.index.item()
idx2 = select2.index.item()
print(idx1)
print(idx2)

selection_df = df.loc[idx1:idx2]

print(selection_df)


