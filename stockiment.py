import api
import sys
import mysql.connector
import time as t
import schedule
import pandas as pd
from investopedia import *
from datetime import *

# Creating a connection to the database for storing information
config = {
    'user': 'root',
    'password': 'root',
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',  # CHANGE PATH
    'database': 'stockiment',
    'raise_on_warnings': True,
    'use_unicode': True,
}

# Getting list of investopedia portfolio stocks -- ENTER ACCOUNT INFO
client = Account("email", "password")


# Returns dictionary of every stock in the database with bullish counts within date range
def getBullishCount(begin_date, end_date):
    bull = dict()

    link = mysql.connector.connect(**config)
    cursor = link.cursor()

    getStocksQuery = ("SELECT DISTINCT sym FROM stocks ")
    cursor.execute(getStocksQuery)

    for stock in cursor:
        bull[stock[0]] = 0

    query = ("SELECT sym FROM stocks "
             "WHERE msg_date BETWEEN %s AND %s "
             "AND bullish = 1 "
             "group by sym, userID ")

    cursor.execute(query, (begin_date, end_date))

    for stock in cursor:
        bull[stock[0]] += 1

    cursor.close()
    link.close()

    return bull


# Returns dictionary of every stock in the database with bearish counts within date range
def getBearishCount(begin_date, end_date):
    bear = dict()

    link = mysql.connector.connect(**config)
    cursor = link.cursor()

    getStocksQuery = ("SELECT DISTINCT sym FROM stocks ")
    cursor.execute(getStocksQuery)

    for stock in cursor:
        bear[stock[0]] = 0

    query = ("SELECT sym FROM stocks "
             "WHERE msg_date BETWEEN %s AND %s "
             "AND bearish = 1 "
             "group by sym, userID ")

    cursor.execute(query, (begin_date, end_date))

    for stock in cursor:
        bear[stock[0]] += 1

    cursor.close()
    link.close()

    return bear


# Returns dictionary of every stock in the database with the total number of bull-bear sentiments
def getBullBearTotal(dict_bull, dict_bear):
    bull_bear_totals = dict()

    for stock in dict_bull:
        bull_bear_totals[stock] = dict_bull[stock] + dict_bear[stock]

    return bull_bear_totals


# Returns dictionary of the bull to bear ratio
def getBullBearRatio(dict_bull, dict_bear):
    bull_bear_ratio = dict()

    for stock in dict_bull:
        if dict_bull[stock] == 0 and dict_bear[stock] == 0:
            bull_bear_ratio[stock] = 0

        elif dict_bull[stock] == 0 and dict_bear[stock] != 0:
            bull_bear_ratio[stock] = 0

        elif dict_bull[stock] != 0 and dict_bear[stock] == 0:
            bull_bear_ratio[stock] = 1

        else:
            bull_bear_ratio[stock] = (float(dict_bull[stock])) / (float(dict_bull[stock] + float(dict_bear[stock])))

    return bull_bear_ratio


# Function that buys 15 shares from X stocks between the date ranges of today to Y days ago
def performBuys(trades, days_ago):

    today = datetime.now()
    before = datetime.now() - timedelta(days=days_ago)
    today = today.strftime("%Y-%m-%d")
    before = before.strftime("%Y-%m-%d")

    # Getting histogram of bullish counts to stock symbol
    bull = getBullishCount(before, today)

    # Getting histogram of bearish counts to stock symbol
    bear = getBearishCount(before, today)

    # Getting histogram of total bullish bearish counts to stock symbol
    total = getBullBearTotal(bull, bear)

    # Getting ratios
    ratio = getBullBearRatio(bull, bear)

    # Appending dictionaries to a dataframe:
    df_bull = pd.DataFrame(data=bull.values(), index=bull.keys(), columns=['Bull'])
    df_bear = pd.DataFrame(data=bear.values(), index=bear.keys(), columns=['Bear'])
    df_total = pd.DataFrame(data=total.values(), index=total.keys(), columns=['Total'])
    df_ratio = pd.DataFrame(data=ratio.values(), index=ratio.keys(), columns=['Ratio'], dtype=float)
    df_all = pd.concat([df_bull, df_bear, df_total, df_ratio], axis=1)

    df_all = pd.DataFrame.sort(df_all, columns='Bull', ascending=False)

    # Buy stock of largest bullish count if ratio is >= .85
    number_of_trades = 0;
    curr_df_row = 0;

    while number_of_trades != trades or curr_df_row == len(df_all['Ratio'])-2:
        if df_all['Ratio'][curr_df_row] >= .85:
            sym = df_all.index.values[curr_df_row]
            print sym
            # noinspection PyBroadException
            try:
                client.trade(str(sym), Action.buy, 500, priceType="Market")
                curr_df_row += 1
                number_of_trades += 1
                continue
            except:
                curr_df_row += 1
                continue
        else:
            curr_df_row += 1

        if curr_df_row >= len(df_all)-2:
            break

    return

def jobMineData():
    today = datetime.now()
    today = today.strftime("%H:%M:%s")
    print "Mining data: " + str(today)
    execfile("sentiment_miner.py")
    print "Finished Job\n"

def jobBuyStocksOne():
    print "Buying stocks"
    performBuys(5, 0)
    print "Finished Job\n"




##################################################################
##################################################################

# Run mining script at 6:00 am
schedule.every().day.at("06:00").do(jobMineData)
schedule.every().day.at("06:30").do(jobMineData)

# Run mining script at 7:00 am
schedule.every().day.at("07:00").do(jobMineData)
schedule.every().day.at("07:30").do(jobMineData)

# Run mining script at 8:00 am
schedule.every().day.at("08:00").do(jobMineData)
schedule.every().day.at("08:30").do(jobMineData)

# Run mining script at 9:00 am
schedule.every().day.at("09:00").do(jobMineData)
schedule.every().day.at("09:30").do(jobMineData)
schedule.every().day.at("09:30").do(jobBuyStocksOne)


# Run mining script at 10:00 am
schedule.every().day.at("10:00").do(jobMineData)
schedule.every().day.at("10:30").do(jobMineData)

# Run mining script at 11:00 am
schedule.every().day.at("11:00").do(jobMineData)
schedule.every().day.at("11:30").do(jobMineData)
schedule.every().day.at("11:30").do(jobBuyStocksOne)


# Run mining script at 12:00 pm
schedule.every().day.at("12:00").do(jobMineData)
schedule.every().day.at("12:30").do(jobMineData)

# Run mining script at 1:00 pm
schedule.every().day.at("13:00").do(jobMineData)
schedule.every().day.at("13:30").do(jobMineData)
schedule.every().day.at("13:30").do(jobBuyStocksOne)

# Run mining script at 2:00 pm
schedule.every().day.at("14:00").do(jobMineData)
schedule.every().day.at("14:30").do(jobMineData)

# Run mining script at 3:00 pm
schedule.every().day.at("15:00").do(jobMineData)
schedule.every().day.at("15:30").do(jobMineData)

# Run mining script at 4:00 pm
schedule.every().day.at("16:00").do(jobMineData)
schedule.every().day.at("16:30").do(jobMineData)

# Run mining script at 5:00 pm
schedule.every().day.at("17:00").do(jobMineData)
schedule.every().day.at("17:30").do(jobMineData)

# Run mining script at 6:00 pm
schedule.every().day.at("18:00").do(jobMineData)
schedule.every().day.at("18:30").do(jobMineData)

# Run mining script at 7:00 pm
schedule.every().day.at("19:00").do(jobMineData)
schedule.every().day.at("19:30").do(jobMineData)

# Run mining script at 8:00 pm
schedule.every().day.at("20:00").do(jobMineData)
schedule.every().day.at("20:30").do(jobMineData)

# Run mining script at 9:00 pm
schedule.every().day.at("21:00").do(jobMineData)
schedule.every().day.at("21:30").do(jobMineData)


while 1:
    schedule.run_pending()
    t.sleep(1)