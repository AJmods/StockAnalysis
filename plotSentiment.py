import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import yfinance as yf
from newsFuncs import getSentiment
from datetime import date, timedelta
import math
import pandas as pd
import numpy as np

import base64
import io



def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def processStockData(ticker, start_date, end_date):

    ticker = yf.Ticker(ticker)

    # get all stock info (slow)
    info = ticker.info
    #print(info)
    #print(info)

    hist = ticker.history(start = start_date, end = end_date)
    dataOverTime = ticker.history_metadata # -> <dict> of data over period
    end_price = dataOverTime['regularMarketPrice']
    start_price = dataOverTime['chartPreviousClose']
    percentage_change = math.floor((end_price/start_price - 1.0) * 100)
    
    #print(dataOverTime)
    print("start price: " + str(start_price))
    print("end price:  " + str(end_price))
    print("percentage change: " + str(percentage_change) + "%")

    name = info["displayName"]

    return (getSentiment(name, start_date, end_date), percentage_change);

def plotStocksAndSentiments(stock, startDate, endDate):
    dates = []
    sentiments = []
    percentChanges = []
    import datetime
    from datetime import date

    start_date = date(int(startDate[0:4]), int(startDate[5:7]), int(startDate[8:10]))
    end_date = date(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]))

    dates =np.arange(np.datetime64(startDate), np.datetime64(endDate), np.timedelta64(24, 'h'))

    for dateThing in daterange(start_date, end_date):
        print()
        #print(dateThing, dateThing+datetime.timedelta(days=1))
        nextDay = dateThing + datetime.timedelta(days=1)
        s, p = processStockData(stock, str(dateThing), str(nextDay));
        sentiments.append(s)
        percentChanges.append(p / 100)

    print(dates)
    print(sentiments)
    print(percentChanges)

    plt.plot(dates, sentiments, label="seniment")
    plt.plot(dates, percentChanges, label="percentChange")
    plt.title(f"{stock} data")
    plt.xlabel("date")
    plt.ylabel("percent")
    plt.legend()
    plt.grid()
    plt.gcf().autofmt_xdate()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    plt.close()
    img = base64.b64encode(img.getvalue()).decode("utf-8").replace("\n", "")

   
    # Embed the result in the html output.
    return f'data:image/png;base64,{img}'

if __name__ == "__main__":
    print(plotStocksAndSentiments("GME","2021-02-01","2021-02-02"))
