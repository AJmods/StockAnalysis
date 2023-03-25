from flask import Flask, render_template, request

import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
import math

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
        processStockData(ticker, start_date, end_date)
        # put
        return "STOCKS are inputed";
    else:
        return render_template("InputStocks.html");

@app.route('/callback/<endpoint>')
def cb(endpoint):   
    if endpoint == "getStock":
        return gm(request.args.get('data'),request.args.get('period'),request.args.get('interval'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        st = yf.Ticker(stock)
        return json.dumps(st.info)
    else:
        return "Bad endpoint", 400

# Return the JSON data for the Plotly graph
def gm(stock,period, interval):
    st = yf.Ticker(stock)
  
    # Create a line graph
    df = st.history(period=(period), interval=interval)
    df=df.reset_index()
    df.columns = ['Date-Time']+list(df.columns[1:])
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date-Time', y="Open",
        hover_data=("Open","Close","Volume"), 
        range_y=(min,max), template="seaborn" )

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def processStockData(ticker, start_date, end_date):

    ticker = yf.Ticker(ticker)

    # get all stock info (slow)
    info = ticker.info
    print(type(info))
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
if __name__ == '__main__':
    app.run()
