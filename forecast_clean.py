import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# https://www.opentechguides.com/how-to/article/pandas/193/index-slice-subset.html
# https://stackoverflow.com/questions/61802727/plotly-trouble-plotting-candlestick-graph-on-a-subplot

START = 57
END = 63

ticker = 'NQ=F'

# forward df
# data = yf.download(tickers=ticker, period='3mo', interval='1d')

df = yf.download(tickers=ticker, period='3mo', interval='1d')
# print(df)
# df.to_csv('orig.csv')

df = df.reset_index()
print(df)
last_row = df.index[-1] + 0.5

# select by index
select3 = df[df.index.isin({START})]  # Choose by index
select4 = df[df.index.isin({END})]  # Choose by index

idx1 = select3.index.item()
idx2 = select4.index.item()

selection_df = df.loc[idx1:idx2]

# df = df.reset_index(drop=True)

# selection_df = df.loc[1:5]

# select = df[df['Low'].isin({14293.5})]  # Choose by a price
select = df[df['Date'].isin({'2022-06-13'})]  # Choose by date

# Choose between 2 dates
# select1 = df[df['Date'].isin({'2022-05-09'})]  # Choose by date
# select2 = df[df['Date'].isin({'2022-05-26'})]  # Choose by date
#
# print(select1)
# print(select2)
#
# idx1 = select1.index.item()
# idx2 = select2.index.item()
# print(idx1)
# print(idx2)
#
# selection_df = df.loc[idx1:idx2]

y0 = max(selection_df['High'])
y1 = min(selection_df['Low'])

x0 = selection_df.index[0] - 0.5
x1 = selection_df.index[-1] + 0.5
length_of_selection = x1 - x0

print(selection_df)
selection_df = selection_df.drop('Date', 1)
print(selection_df)
selection_df = selection_df.reset_index(drop=True)
print(selection_df)
last_row_select = selection_df.index[-1] + 1
print(last_row_select)
# selection_df.set_index('Date', inplace=True)


# take difference between 'high' of first df first row and second df last row
df_high = df['High'].iloc[-1]        # get last row of our starting point
selection_df_high = selection_df['High'].iloc[0]       # get first row of selection
# selection_df_high = selection_df['High'].iloc[-1]       # get last row of selection for reversal
diff = selection_df_high - df_high
print(diff)

# selection_df = selection_df.reset_index(drop=True)
# print(selection_df)

selection_df -= diff
print(selection_df)

# # use for reversal
# selection_df = selection_df.iloc[::-1]

df = df.drop('Date', 1)
print(df)

frames = [df, selection_df]
symmetric_df = pd.concat(frames)

symmetric_df = symmetric_df.reset_index(drop=True)

print(symmetric_df)
forecast_df = symmetric_df.tail(last_row_select)
print(forecast_df)

fig = go.Figure(data=[go.Candlestick(x=df.index,
                                      open=df['Open'],
                                      high=df['High'],
                                      low=df['Low'],
                                      close=df['Close'], showlegend=False)])


fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['High'], line=dict(color='#0000ff', width=5)))

fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['Low'], line=dict(color='#0000ff', width=5)))

fig.add_vline(x=last_row, line_width=3, line_dash="dash", line_color="green")

fig.add_shape(type="rect",
    x0=x0, y0=y0, x1=x1, y1=y1,
    line=dict(color="RoyalBlue"),)

# https://plotly.com/python/reference/layout/annotations/
# https://stackoverflow.com/questions/62716521/plotly-how-to-add-text-to-existing-figure
text_spacer = 6

fig.add_annotation(text='Actuals', x=last_row - text_spacer, y=15000, showarrow=False, font_size=20)

fig.add_annotation(text='Forecast', x=last_row + text_spacer, y=15000, showarrow=False, font_size=20)

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
