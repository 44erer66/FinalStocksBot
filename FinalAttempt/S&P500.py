import bs4 as bs
import pickle

import requests
import pandas as pd

def save_sp500_tickers():
    resp = requests.get('https://swingtradebot.com/equities?min_vol=0&min_price=2.0&max_price=500.0&adx_trend=up&grade=A&include_etfs=0&html_button=as_html')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    print(soup)
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        x = ticker.split("\n")[0]
        tickers.append(x)
    print(tickers)
    lis = {"Symbol":tickers}
    df = pd.DataFrame(lis)
    df.to_csv('S&P500.csv')

save_sp500_tickers()