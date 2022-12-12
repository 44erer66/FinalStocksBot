import pandas as pd
import numpy as np

def ExpMovingAverage(values, window):
    try:
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()

        a = np.convolve(values, weights)[:len(values)]
        a[:window] = a[window]
        return a[-1]
    except:
        return -1000
import pickle
with open("Crypto.pickle", "rb") as f:
    model = pickle.load(f)
def RSI(prices2):
    dayGains = []
    dayLosses = []
    if len(prices2) > 14:
        prices = prices2[-14:]
        pos = len(prices) - 1
        price = prices[pos]

        for pos2, price2 in enumerate(prices):
            if pos2 == 0:
                dayGains.append(0)
                dayLosses.append(0)
            else:
                if price2 - prices[pos2 - 1] > 0:
                    dayGains.append(abs(price2 - prices[pos2 - 1]))
                    dayLosses.append(0)
                elif price2 - prices[pos2 - 1] < 0:
                    dayGains.append(0)
                    dayLosses.append(abs(price2 - prices[pos2 - 1]))
                else:
                    dayGains.append(0)
                    dayLosses.append(0)

        dayRSI = []
        last14G = dayGains
        last14L = dayLosses


        avgG = sum(last14G) / len(last14L)
        avgL = sum(last14L) / len(last14L)
        val = (avgG + dayGains[pos]) / (avgL + dayLosses[pos])
        dayRSI.append(100 - (100 / (1 + val)))



        return dayRSI
    else:
        return [0]
def SMA(prices, lookBack):
    daySMA = []
    pos = len(prices) - 1
    if pos < lookBack:
        daySMA.append(0)
    else:
        daySMA.append(sum(prices[pos - lookBack:pos + 1]) / lookBack)
    return daySMA
def SO(prices):
    daySO = []
    pos = len(prices) - 1
    price = prices[pos]

    if pos < 14:
        daySO.append(0)
    else:
        value = ((price - min(prices[pos - 14:pos + 1])) / (
                    max(prices[pos - 14:pos + 1]) - min(prices[pos - 14:pos + 1]))) * 100
        daySO.append(value)
    return daySO
def buyFunc(prices):

    try:
        rsi = RSI(prices)[0]
        MACD = ExpMovingAverage(prices, 12) - ExpMovingAverage(prices, 26)
        lMACD = ExpMovingAverage(prices[:-1], 12) - ExpMovingAverage(prices[:-1], 26)
        EMA200 = ExpMovingAverage(prices, 200)
        #print(EMA200)
        if EMA200 > prices[-1] and rsi < 30 and model.predict([[rsi, SMA(prices, 8)[0], SMA(prices, 8)[0], SO(prices)[0], ExpMovingAverage(prices, 200)]]) == 1:

            return True
        else:
            return False
    except:
        return False

import time

prices = []
iteration = 10

from datetime import datetime
import requests
pd.set_option('expand_frame_repr', False)
def get_current_data(from_sym='BTC', to_sym='USD', exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price'

    parameters = {'fsym': from_sym,
                  'tsyms': to_sym}

    if exchange:
        #print('exchange: ', exchange)
        parameters['e'] = exchange

    # response comes as json
    response = requests.get(url, params=parameters)
    data = response.json()

    return data

money = 500
leverage = 1
isBought = False
BoughtAt = 0


while True:

    currentPrice = get_current_data('ETH','USD','coinbase')
    print(currentPrice)
    prices.append(currentPrice)
    if isBought == False:
        isBuy = buyFunc(prices)

        if isBuy == True:
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print("We BOUGHT Ethereum at ",current_time , " for ", currentPrice)
            print("We managed to buy ", money/currentPrice, " of Ethereum")
            print(money)
            print()
            BoughtAt = currentPrice
            isBought = True
    else:
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        if currentPrice >= BoughtAt*1.02:

            print("We SOLD Ethereum at ", current_time, " for ", currentPrice)
            isBought = False
            BoughtAt = 0

            money += money*  (1+((1-currentPrice/BoughtAt)*leverage))


        if currentPrice <= BoughtAt*0.98:
            print("We SOLD Ethereum at ", current_time, " for ", currentPrice)
            isBought = False
            BoughtAt = 0

            money += money * (1 + ((1 - currentPrice / BoughtAt) * leverage))
            print(money)
    time.sleep(600)


