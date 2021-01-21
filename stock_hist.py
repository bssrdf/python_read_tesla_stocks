import yahoo_fin.stock_info as si

import requests

import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

tickers = ['BABA', 'AAPL', 'TSLA']
stockname = []
for ticker in tickers:
    stock_company = f"https://finance.yahoo.com/quote/{ticker.lower()}"
    soup = BeautifulSoup(requests.get(stock_company).text, "html.parser")
    name = soup.h1.text.split('(')[0].strip()
    ticker_data_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
    ticker_data = json.loads(requests.get(ticker_data_url).text)
    price = ticker_data['chart']['result'][0]['meta']['previousClose']
    if name:
        stockname.append( [ticker, name, price] )

pprint(stockname, width=60)

#for ticker in tickers
#    prices[ticker] = si.get_data(ticker)

#print(prices['AAPL'])