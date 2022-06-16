# https://www.datasciencemadesimple.com/reverse-the-rows-of-the-dataframe-in-pandas-python-2/

import pandas as pd
import numpy as np

df1 = {
    'State':['Arizona AZ','Georgia GG','Newyork NY','Indiana IN','Florida FL'],
   'Score':[62,47,55,74,31]}

df1 = pd.DataFrame(df1, columns=['State', 'Score'])
print(df1)

df2 = df1.iloc[::-1]
print(df2)
