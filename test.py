#!/usr/bin/env python

import pandas as pd
import datetime
#import pandas.io.data as web
import matplotlib.pyplot as plt
from matplotlib import style
from pandas_datareader import data, wb

style.use('ggplot')

start = datetime.datetime(2010,1,1)
end = datetime.datetime(2017,7,26)
df = wb.DataReader('XOM', 'yahoo', start, end)

print(df.head())
df['Adj Close'].plot()
plt.show()
