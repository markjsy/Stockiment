# Stockiment
A few scripts I hacked together in a weekend to track how public sentiment (tweets) correlates with public sentiment


## api.py ##
  StockTwits API allows you to use their REST service
  
## investopedia.py ##
  Investopedia API allows you to access Investopedia website to buy/sell mock stocks

## prediction_toolkit.py ##
  Get dataframe of longterm sentiment from Quandl datasource

## sentiment_miner.py ##
  Quanitfies sentiment score from current portfolio as well as top trending stocks from StockTwits and adds to database

## stockiment ##
  Buys the top stocks (highest sentiment) on investopedia. Runs a cronjob periodically.
