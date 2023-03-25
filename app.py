from flask import Flask, render_template, request

import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
import math

from newsFuncs import getSentiment

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return "Hello World"

@app.route('/stockAnalysis', methods=["GET", "POST"])
def stockAnalysis():
    if request.method == "POST":
        print(request.form["stock"])
        print(request.form["startDate"])
        print(request.form["endDate"])
        
        ticker = request.form["stock"]
        start_date = request.form["startDate"]
        end_date = request.form["endDate"]

        # Put stock analysis method here
        sentiment, percentChange = processStockData(ticker, start_date, end_date)
        return render_template("InputStocks.html", message=f"{ticker} had a {percentChange}% percent change with a sentiment score of {sentiment}");
    else:
        return render_template("InputStocks.html");

def processStockData(ticker, start_date, end_date):

    ticker = yf.Ticker(ticker)

    # get all stock info (slow)
    info = ticker.info
    print(info)
    #print(info)

    hist = ticker.history(start = start_date, end = end_date)
    dataOverTime = ticker.history_metadata
    end_price = dataOverTime['regularMarketPrice']
    start_price = dataOverTime['chartPreviousClose']
    percentage_change = math.floor((end_price/start_price - 1.0) * 100)
    
    #print(dataOverTime)
    print("start price: " + str(start_price))
    print("end price:  " + str(end_price))
    print("percentage change: " + str(percentage_change) + "%")

    name = info["displayName"]

    return (getSentiment(name, start_date, end_date), percentage_change);
    
if __name__ == '__main__':
    app.run()
