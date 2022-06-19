import yfinance as yf
import plotly.graph_objects as go

# https://www.opentechguides.com/how-to/article/pandas/193/index-slice-subset.html
# https://stackoverflow.com/questions/61802727/plotly-trouble-plotting-candlestick-graph-on-a-subplot

START = 98
END = 119
TARGET = 120

ticker = 'NQ=F'

df = yf.download(tickers=ticker, period='12mo', interval='1d')

df = df.reset_index()
print(df)
last_row = df.index[-1] + 0.5

# select by index
select3 = df[df.index.isin({START})]  # Choose by index
select4 = df[df.index.isin({END})]  # Choose by index

idx1 = select3.index.item()
idx2 = select4.index.item()

selection_df = df.loc[idx1:idx2]

# coordinates for the rectangle

y0 = max(selection_df['High'])
y1 = min(selection_df['Low'])

x0 = selection_df.index[0] - 0.5
x1 = selection_df.index[-1] + 0.5

length_of_selection = x1 - x0 - 1       # this is for deriving size of target range

selection_df = selection_df.drop('Date', 1)
selection_df = selection_df.reset_index(drop=True)
last_row_select = selection_df.index[-1] + 1

forecast_range_start = TARGET
forecast_range_end = forecast_range_start + length_of_selection

# select by index
select5 = df[df.index.isin({forecast_range_start})]  # Choose by index
select6 = df[df.index.isin({forecast_range_end})]  # Choose by index

idx5 = select5.index.item()
idx6 = select6.index.item()

forecast_range_df = df.loc[idx5:idx6]
print(forecast_range_df)
y5 = max(forecast_range_df['High'])
y6 = min(forecast_range_df['Low'])

x5 = forecast_range_df.index[0] - 0.5
x6 = forecast_range_df.index[-1] + 0.5

df_high = forecast_range_df['High'].iloc[0]            # get first row of forecast range
selection_df_high = selection_df['High'].iloc[0]       # get first row of selection
diff = selection_df_high - df_high                      # get the diff
print(diff)

selection_df -= diff                                    # adjust selection by diff to match levels of forecast range
print(selection_df)

df = df.drop('Date', 1)
print(df)

fig = go.Figure(data=[go.Candlestick(x=df.index,
                                      open=df['Open'],
                                      high=df['High'],
                                      low=df['Low'],
                                      close=df['Close'], showlegend=False)])


fig.add_trace(go.Scatter(x=forecast_range_df.index, y=selection_df['High'], line=dict(color='#0000ff', width=5), name='forecast'))

fig.add_trace(go.Scatter(x=forecast_range_df.index, y=selection_df['Low'], line=dict(color='#0000ff', width=5), name='forecast'))

fig.add_shape(type="rect",
    x0=x0, y0=y0, x1=x1, y1=y1,
    line=dict(color="RoyalBlue"),)

fig.add_shape(type="rect",
    x0=x5, y0=y5, x1=x6, y1=y6,
    line=dict(color="darkred"),)


# https://plotly.com/python/reference/layout/annotations/
# https://stackoverflow.com/questions/62716521/plotly-how-to-add-text-to-existing-figure
fig.update_layout(
    title=ticker, xaxis_rangeslider_visible=False)

fig.write_html( 'output_file_name.html',
                   auto_open=True )

