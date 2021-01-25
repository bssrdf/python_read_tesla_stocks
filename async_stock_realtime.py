import yahoo_fin.stock_info as si


import requests
import time
import aiohttp
from bs4 import BeautifulSoup
import json
from pprint import pprint
import asyncio
#tickers = ['BABA', 'AAPL', 'TSLA', 'FB', 'GOOG', 'TWTR', 'GM','CIDM']
stockname = []
import json


async def printStockInfo(ticker):
    async with aiohttp.ClientSession() as session:
        url = f"https://finance.yahoo.com/quote/{ticker.lower()}"
        async with session.get(url) as resp:
            text = await resp.read()
    async with aiohttp.ClientSession() as session:
        ticker_data_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
        async with session.get(ticker_data_url) as resp:
            price_text = await resp.read()
    soup = BeautifulSoup(text.decode('utf-8'), 'html.parser')
    name = soup.h1.text.split('(')[0].strip()
    ticker_data = json.loads(price_text)
    price = ticker_data['chart']['result'][0]['meta']['previousClose']
    print([ticker, name, price])

tasks = []
event_loop = asyncio.get_event_loop()

with open("stocks.json", "r") as read_file:
    tickers = json.load(read_file)
    #print(stocks)
    #started = time.time()
    for ticker in tickers['stocks']:
        tasks.append((printStockInfo(ticker)))
    #elapsed = time.time()
    #print("Time taken: ", elapsed-started)
started = time.time()
event_loop.run_until_complete(asyncio.wait(tasks))
event_loop.close()
elapsed = time.time()
print("Time taken: ", elapsed-started)    
#pprint(stockname, width=60)

#for ticker in tickers
#    prices[ticker] = si.get_data(ticker)

#print(prices['AAPL'])
