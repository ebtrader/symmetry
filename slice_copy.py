import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# https://www.opentechguides.com/how-to/article/pandas/193/index-slice-subset.html

ticker = 'NQ=F'

# forward df
data = yf.download(tickers=ticker, period='3mo', interval='1d')
df = yf.download(tickers=ticker, period='3mo', interval='1d')
print(df)
df.to_csv('orig.csv')



df = df.reset_index()

# df = df.reset_index(drop=True)

# selection_df = df.loc[1:5]

# select = df[df['Low'].isin({14293.5})]  # Choose by a price
select = df[df['Date'].isin({'2022-06-13'})]  # Choose by date

# Choose between 2 dates
select1 = df[df['Date'].isin({'2022-05-09'})]  # Choose by date
select2 = df[df['Date'].isin({'2022-05-26'})]  # Choose by date

print(select1)
print(select2)

idx1 = select1.index.item()
idx2 = select2.index.item()
print(idx1)
print(idx2)

selection_df = df.loc[idx1:idx2]

print(selection_df)
selection_df = selection_df.drop('Date', 1)
print(selection_df)

# selection_df.set_index('Date', inplace=True)


# take difference between 'high' of first df first row and second df last row
df_high = df['High'].iloc[-1]        # get last row of our starting point
selection_df_high = selection_df['High'].iloc[0]       # get first row of selection
diff = selection_df_high - df_high
print(diff)

# selection_df = selection_df.reset_index(drop=True)
# print(selection_df)

selection_df -= diff
print(selection_df)

df = df.drop('Date', 1)
print(df)

frames = [df, selection_df]
symmetric_df = pd.concat(frames)
symmetric_df = symmetric_df.reset_index(drop=True)

print(symmetric_df)
# symmetric_df.to_csv('new_chart.csv')

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

# fig1 = go.Figure(data=[go.Candlestick(x=data.index,
#                                       open=data['Open'],
#                                       high=data['High'],
#                                       low=data['Low'],
#                                       close=data['Close'], showlegend=False)])
#
# fig1.update_layout(
#     title=ticker, xaxis_rangeslider_visible=False)
#
# fig1.write_html( 'output_file_name1.html',
#                    auto_open=True )
#
#
#
