import pandas as pd
import numpy as numpy
import math
import quandl
import datetime
import time
import sklearn
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import SGDRegressor

# Getting useful dataframes
df_sentiment = quandl.get("AAII/AAII_SENTIMENT", authtoken="Wssko8sPk-zv6xa8631A")

# Returns dataframe of stock symbol
# ['Adj. Low', 'Adj. High', 'Adj. Close', 'Adj Open']
def getStock(sym):
    return quandl.get("WIKI/"+sym, authtoken="Wssko8sPk-zv6xa8631A" )

def appendPriceTrendToDF(df):
    # Calculating trend based on slope

    df_size = df['Adj. Close'].size
    d_ind = 0
    trend = list()

    while d_ind + 1 != df_size:
        y1 = df['Adj. Close'][d_ind]
        y2 = df['Adj. Close'][d_ind + 1]
        x1 = d_ind
        x2 = d_ind + 1

        m = (y2 - y1) / (x2 - x1)

        trend.append(m)
        d_ind += 1

    trend = numpy.asarray(trend)
    trend = numpy.insert(trend, 0, 1)

    date = df['Adj. Close'].index
    date = date.rename('Date')
    trend = pd.Series(trend, date, name='Price Trend')

    # Appending Price Trend
    df = df.join(trend)
    return df

def appendLongTermSentimentToDF(df):
    return pd.concat([df, df_sentiment], axis=1)



