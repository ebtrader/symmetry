import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

ticker = 'NQ=F'

# forward df
df1 = yf.download(tickers=ticker, period='3mo', interval='1d')
print(df1)

# reverse df
df2 = df1.iloc[::-1] # reverse rows
print(df2)

# concat df
frames = [df1, df2]
symmetric_df = pd.concat(frames)
print(symmetric_df)

# drop index
symmetric_df = symmetric_df.reset_index(drop=True)
print(symmetric_df)

fig = go.Figure(data=[go.Candlestick(x=symmetric_df.index,
                                      open=symmetric_df['Open'],
                                      high=symmetric_df['High'],
                                      low=symmetric_df['Low'],
                                      close=symmetric_df['Close'], showlegend=False)])

fig.add_vline(x=64.5, line_width=3, line_dash="dash", line_color="green")

# https://plotly.com/python/reference/layout/annotations/
# https://stackoverflow.com/questions/62716521/plotly-how-to-add-text-to-existing-figure

fig.add_annotation(text='Actuals', x=54, y=15000, showarrow=False, font_size=20)

fig.add_annotation(text='Forecast', x=75, y=15000, showarrow=False, font_size=20)

fig.update_layout(
    title=ticker, xaxis_rangeslider_visible=False)

fig.write_html( 'output_file_name.html',
                   auto_open=True )

