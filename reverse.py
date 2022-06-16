# https://www.datasciencemadesimple.com/reverse-the-rows-of-the-dataframe-in-pandas-python-2/

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df1 = {
    'State':['Arizona AZ','Georgia GG','Newyork NY','Indiana IN','Florida FL'],
   'Score':[62,47,55,74,31]}

df1 = pd.DataFrame(df1, columns=['State', 'Score'])
print(df1)

df2 = df1.iloc[::-1]
print(df2)

# https://www.geeksforgeeks.org/how-to-combine-two-dataframe-in-python-pandas/

frames = [df1, df2]

result = pd.concat(frames)

print(result)

# https://www.machinelearningplus.com/pandas/pandas-reset-index/

result = result.reset_index(drop=True)

print(result)

fig = px.scatter(result, x=result.index, y="Score")

fig.write_html( 'output_file_name.html',
                   auto_open=True )

# fig1 = go.Figure(data=[go.Candlestick(x=df['Date'],
#                                       open=df['Open'],
#                                       high=df['High'],
#                                       low=df['Low'],
#                                       close=df['Close'], showlegend=False)])
#
# fig1.write_html( 'output_file_name.html',
#                    auto_open=True )
