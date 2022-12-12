import json
import time
import requests
import pickle
import alpaca_trade_api as tradeapi
import datetime
import numpy as np
# defining key/request url

key = "AKH3R964QCZO3M4XMHTL"
sec = "Gmxy44G6Q0EpagU5ndARSNdwmVZzBtOflxNmxbou"
url = "https://api.alpaca.markets"
api = tradeapi.REST(key, sec, url, api_version='v2')
account = api.get_account()

def pull_price(symbol):
    key = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

    # requesting data from url
    data = requests.get(key)
    data = data.json()
    return data['price']
#rint(pull_price('ETHUSDT'))
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
def OBV(prices):
    dayOBV = []
    prev = 0
    pos = len(prices) - 1
    price = prices[pos]

    if price > prev:
        dayOBV.append(price)
    elif price == prev:
        dayOBV.append(0)
    else:
        dayOBV.append(-price)
    return dayOBV
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
def WR(prices):
    dayWilliamR = []

    pos = len(prices) - 1
    price = prices[pos]

    if pos < 14:
        dayWilliamR.append(0)
    else:
        value = (max(prices[pos - 14:pos + 1]) - price) / (max(prices[pos - 14:pos + 1]) - min(prices[pos - 14:pos + 1]))
        dayWilliamR.append(value)
    return dayWilliamR





def buyStock(symbol, amt):
    api.submit_order(symbol=symbol,
                     notional=amt,
                     side="buy",
                     type="market",
                     time_in_force="gtc")


def sellStock(symbol, amt):
    api.submit_order(symbol=symbol,
                     notional=amt,
                     side="sell",
                     type="market",
                     time_in_force="gtc")

with open("Crypto.pickle", "rb") as f:
    model = pickle.load(f)

prices = []
isBought = False
BoughtAt = None
x = False
while True:

    curr = float(pull_price('ETHUSDT'))
    #buyStock('ETHUSD', 450)
    prices.append(curr)
    h, m = int(datetime.datetime.now().strftime("%H")), int(datetime.datetime.now().strftime("%M"))

    if not isBought:
        try:
            inputs = [[RSI(prices)[0], SMA(prices, 8)[0], SMA(prices, 14)[0], SO(prices)[0], WR(prices)[0]]]
            x = True
        except:
            print("error")
        if x:
            pred = model.predict(inputs)
            print(pred)
            if pred == 1:

                buyStock('ETHUSD', 430)
                print("We bought a crypto")
                isBought = True
                BoughtAt = curr
                BoughtTime = h*100+m
            else:
                time.sleep(56)
            x = False

    else:
        if h*100 +m > BoughtTime+10:
            sellStock('ETHUSD', 430)
            print("We sold the crypto at ", curr-BoughtAt)
            isBought = False
        elif curr > BoughtAt*1.006:
            sellStock('ETHUSD', 430)
            isBought = False


