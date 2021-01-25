import yahoo_fin.stock_info as si


import requests
import time
from bs4 import BeautifulSoup
import json
from pprint import pprint
import asyncio
#tickers = ['BABA', 'AAPL', 'TSLA', 'FB', 'GOOG', 'TWTR', 'GM','CIDM']
stockname = []
import json

def printStockInfo(ticker):
    stock_company = f"https://finance.yahoo.com/quote/{ticker.lower()}"
    soup = BeautifulSoup(requests.get(stock_company).text, "html.parser")
    name = soup.h1.text.split('(')[0].strip()
    ticker_data_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
    ticker_data = json.loads(requests.get(ticker_data_url).text)
    price = ticker_data['chart']['result'][0]['meta']['previousClose']
    if name:
        #stockname.append( [ticker, name, price] )
        print([ticker, name, price])


with open("stocks.json", "r") as read_file:
    tickers = json.load(read_file)
    #print(stocks)
    started = time.time()
    for ticker in tickers['stocks']:
        printStockInfo(ticker)
    elapsed = time.time()
    print("Time taken: ", elapsed-started)
#    prices[ticker] = si.get_data(ticker)

#print(prices['AAPL'])
