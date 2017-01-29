# -*- coding: utf-8 -*-
import api
import sys
import mysql.connector
import time
from investopedia import *
from datetime import date, datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

# Creating a connection to the database for storing information
config = {
    'user': 'root',
    'password': 'root',
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'database': 'stockiment',
    'raise_on_warnings': True,
    'use_unicode':True,
}
link = mysql.connector.connect(**config)
cursor = link.cursor()

# Enforce UTF-8 for the connection.
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")

# Getting a list of trending stocks
trending_stocks = api.get_trending_stocks()

trending_stock_symbols = [stock['symbol'] for stock in trending_stocks]

# Getting list of investopedia portfolio stocks
client = Account("email", "pass")       # CHANGE ME
status = client.get_portfolio_status()
portfolio = status.portfolio


# Appending trending stocks with current portfolio
trending_stock_symbols = list(set(portfolio + trending_stock_symbols))
print trending_stock_symbols

# Dictionary: Holds stream data
stock_stream = dict()
# Dictionary: Holds sentiment score
stock_sentiment_score = dict()

# Gets entire stream and sets default sentiment score of 0
for stock in trending_stock_symbols:
    stock_stream[stock] = api.get_stock_stream(stock)
    stock_sentiment_score[stock] = [0, 0, 0]

# Extracting messages[0], date[1], sentiment[2], msg_id[3], 'user_id[4]
for stock in stock_stream:
    stream = stock_stream[stock]
    mds = []

    for i in range(0, len(stream['messages'])-1):
        inner = []
        # 0
        inner.append(stream['messages'][i]['body'])
        # 1
        inner.append(str(stream['messages'][i]['created_at']).split('T')[0])
        # 2
        inner.append(stream['messages'][i]['entities']['sentiment'])
        # 3
        inner.append(int(stream['messages'][i]['id']))
        # 4
        inner.append(int(stream['messages'][i]['user']['id']))

        mds.append(inner)

    stock_stream[stock] = mds

print str(stock_stream)


# Adding collected data to database
for stock in stock_stream:
    stream = stock_stream[stock]
    for mds in stream:
        add_stock_info = None

        if mds[2] is not None:
            sentiment = mds[2]
            basic = sentiment['basic']

            if basic == 'Bullish':
                add_stock_info = ("INSERT IGNORE INTO stocks "
                                  "(msg_date, sym, userID, msgID, body, bullish) "
                                  "VALUES (%s, %s, %s, %s, %s, %s)")
                date = datetime.strptime( mds[1], "%Y-%m-%d")
                data = (date, stock, mds[4], mds[3], mds[0].decode('utf-8'), 1)
                cursor.execute(add_stock_info, data)

            elif basic == 'Bearish':
                add_stock_info = ("INSERT IGNORE INTO stocks "
                                  "(msg_date, sym, userID, msgID, body, bearish) "
                                  "VALUES (%s, %s, %s, %s, %s, %s)")

                date = datetime.strptime( mds[1], "%Y-%m-%d")
                data = (date, stock, mds[4], mds[3], mds[0].decode('utf-8'), 1)
                cursor.execute(add_stock_info, data)

        else:
            add_stock_info = ("INSERT IGNORE INTO stocks "
                              "(msg_date, sym, userID, msgID, body, neutral) "
                              "VALUES (%s, %s, %s, %s, %s, %s)")
            date = datetime.strptime( mds[1], "%Y-%m-%d")
            data = (date, stock, mds[4], mds[3], mds[0].decode('utf-8'), 1)
            cursor.execute(add_stock_info, data)

        # Committing data to database
        link.commit()

cursor.close()
link.close()





