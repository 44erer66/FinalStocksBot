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

def HVI(volumes):
    volumes2 = volumes[-10:]
    HV = max(volumes2)
    HVI = volumes[-1] * 100 / HV
    return HVI

def buyFunc(prices, volumes):

    try:
        rsi = RSI(prices)[0]
        MACD = ExpMovingAverage(prices, 12) - ExpMovingAverage(prices, 26)
        lMACD = ExpMovingAverage(prices[:-1], 12) - ExpMovingAverage(prices[:-1], 26)
        EMA200 = ExpMovingAverage(prices, 200)
        hvi = HVI(volumes)
        #model.predict([[rsi, SMA(prices, 8)[0], SMA(prices, 14)[0], SO(prices)[0], ExpMovingAverage(prices, 200)]]) == 1
        inputs = [rsi, ExpMovingAverage(prices, 200), MACD]
        for i in range(2, 11):
            inputs.append(prices[-i]/EMA200)
        if 5 < model.predict([inputs]) < 60:

            return True
        else:
            return False
    except:
        return False


df = pd.read_csv('Binance_ETHUSDT_2022_minute.csv')

prices = list(df['open'])[0:141160][::-1][::10]

volumes = list(df['Volume USDT'])[0:141160][::-1][::1]
#print(len(df['open']))
TakeProfit, StopLoss = 2, 1
visitedPrices = []
visitedVolumes = []
Trades = []
numberOfTrades = 0
isBought = False
BoughtAt = 0
wins = 0
losses = 0
profit = []

for pos,price in enumerate(prices):

    visitedPrices.append(price)
    visitedVolumes.append(volumes[pos])
    if not isBought:
        if buyFunc(visitedPrices, visitedVolumes):

            BoughtAt = price
            isBought = True
    else:

        if 1 - (StopLoss/100) < price/BoughtAt < 1 + (TakeProfit/100):
            pass
        else:

            Trades.append((BoughtAt, price))

            if price - BoughtAt < 0:
                profit.append(0)
                losses+=1
            else:
                profit.append(1)
                wins+=1

            isBought = False
            BoughtAt = 0
            numberOfTrades += 1

print(numberOfTrades)
print(wins, losses)
