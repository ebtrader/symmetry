# https://stackoverflow.com/questions/61802727/plotly-trouble-plotting-candlestick-graph-on-a-subplot

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

N=14
df = pd.DataFrame({'Open': np.random.randint(1,29,N),
                   'Close': np.random.randint(1,29,N),
                   'Low': np.random.randint(1,29,N),
                   'High': np.random.randint(1,29,N),
                   'Action': np.random.choice(['sell', 'buy'],N),
                   'System Quality Number': np.random.randint(1,29,N)})


fig = make_subplots(rows=3, cols=1)

fig.add_trace(go.Candlestick(x = df.index,
                            open = df['Open'],
                            close = df['Close'],
                            low = df['Low'],
                            high = df['High']),
             row = 1, col = 1)

fig.add_trace(go.Scatter(x = df.index, y = df['System Quality Number']),
                         row = 2, col = 1)

fig.add_trace(go.Scatter(x = df.index, y = df['Action']), row = 3, col =1)

fig.update_xaxes(row=1, col=1, rangeslider_thickness=0.05)
fig.update_layout(width=900, height=900, xaxis_rangeslider_visible=False)

fig.write_html( 'output_file_name.html',
                   auto_open=True )

