# Stockiment
A few scripts I hacked together in a weekend to track how public sentiment (tweets) correlates with market sentiment


## api.py ##
  StockTwits API allows you to use their REST service
  
## investopedia.py ##
  Investopedia API allows you to access Investopedia website to buy/sell mock stocks

## prediction_toolkit.py ##
  Get dataframe of longterm sentiment from Quandl datasource

## sentiment_miner.py ##
  Does the scraping and quanitfies sentiment score using current portfolio as well as top trending stocks from StockTwits.

## stockiment ##
  Buys the top stocks (highest sentiment) on Investopedia.
