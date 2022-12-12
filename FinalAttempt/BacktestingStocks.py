
#IMPORTS
import pandas as pd
from datetime import datetime
import yfinance as yf
import numpy as np
import pickle
import typing
#IMPORTS

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



        return dayRSI[0]
    else:
        return 0
import typing

def wilders_rsi(data: list, window_length: int,
                use_rounding: bool = True) -> typing.List[typing.Any]:
    """
    A manual implementation of Wells Wilder's RSI calculation as outlined in
    his 1978 book "New Concepts in Technical Trading Systems" which makes
    use of the α-1 Wilder Smoothing Method of calculating the average
    gains and losses across trading periods.
    @author: https://github.com/alphazwest
    Args:
        data: List[float or int] - a collection of floating point values
        window_length: int-  the number of previous periods used for RSI calculation
        use_rounding: bool - option to round calculations to the nearest 2 decimal places
    Returns:
        A list object with len(data) + 1 members where the first is a header as such:
             ['date', 'close', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rsi']
    """

    # Define a rounding function based on argument
    do_round = lambda x: round(x, 2) if use_rounding else x  # noqa: E731

    # Define containers
    gains: typing.List[float]       = []
    losses: typing.List[float]      = []
    window: typing.List[float]      = []

    # Define convenience variables
    prev_avg_gain: float or None    = None
    prev_avg_loss: float or None    = None

    # Define output container with header
    output: typing.List[typing.Any] = [
        ['date', 'close', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rsi']
    ]
    for i, price in enumerate(data):

        # Skip first row but remember price
        if i == 0:
            window.append(price)
            output.append([i+1, price, 0, 0, 0, 0, 0])
            continue

        # Calculate price difference with previous period
        difference = do_round(data[i] - data[i - 1])

        # Record positive differences as gains, negative as losses
        if difference > 0:
            gain = difference
            loss = 0
        elif difference < 0:
            gain = 0
            loss = abs(difference)
        else:
            gain = 0
            loss = 0
        gains.append(gain)
        losses.append(loss)

        # Don't calculate averages until n-periods data available
        if i < window_length:
            window.append(price)
            output.append([i+1, price, gain, loss, 0, 0, 0])
            continue

        # Calculate Average for first gain as SMA
        if i == window_length:
            avg_gain = sum(gains) / len(gains)
            avg_loss = sum(losses) / len(losses)

        # Use WSM after initial window-length period
        else:
            avg_gain = (prev_avg_gain * (window_length - 1) + gain) / window_length
            avg_loss = (prev_avg_loss * (window_length - 1) + loss) / window_length

        # Round for precision
        avg_gain = do_round(avg_gain)
        avg_loss = do_round(avg_loss)

        # Keep in memory
        prev_avg_gain = avg_gain
        prev_avg_loss = avg_loss

        # Calculate RS
        rs = do_round(avg_gain / avg_loss)

        # Calculate RSI
        rsi = do_round(100 - (100 / (1 + rs)))

        # Remove oldest values
        window.append(price)
        window.pop(0)
        gains.pop(0)
        losses.pop(0)

        # Save Data
        output.append(rsi)

    return output[-1]

def SMA(prices, lookBack):
    daySMA = []
    pos = len(prices) - 1
    if pos < lookBack:
        daySMA.append(0)
    else:
        daySMA.append(sum(prices[pos - lookBack:pos + 1]) / lookBack)
    return daySMA[0]
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
    return dayOBV[0]
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
    return daySO[0]
def WR(prices):
    dayWilliamR = []

    pos = len(prices) - 1
    price = prices[pos]

    if pos < 14:
        dayWilliamR.append(0)
    else:
        value = (max(prices[pos - 14:pos + 1]) - price) / (max(prices[pos - 14:pos + 1]) - min(prices[pos - 14:pos + 1]))
        dayWilliamR.append(value)
    return dayWilliamR[0]

def ExpMovingAverage(values, window):
    try:
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()

        a = np.convolve(values, weights)[:len(values)]
        a[:window] = a[window]
        return a[-1]
    except:
        return 1/0
losses = []
dubs = []
data2 = pd.read_csv('S&P500.csv')
symbols = list(data2["Symbol"])
money = 1000
finalso = []
finalsa = []
for pos, symbol in enumerate(['AAPL']):

        stockData = pd.read_csv('/Users/44erer66/Desktop/StockBot/TestingData/'+symbol+'.csv')
        with open("/Users/44erer66/Desktop/StockBot/Agents/"+symbol+".pickle", "rb") as f:
            modelo = pickle.load(f)
        with open('DTagent.pickle', 'rb') as f:
            model2 = pickle.load(f)
        prices = []
        modelOutputs = []
        naturalOutputs = []
        winLoss = []
        for day in range(len(stockData['High'])-1):

            if day > 200:

                curr = []
                #print(prices)
                EMA200 = ExpMovingAverage(prices, 200)

                for i in range(0, 8):
                    #curr.append(stockData["High"][day - i] / EMA200)  # HIGH
                    #curr.append(stockData["Low"][day - i] / EMA200)  # LOW
                    #curr.append(stockData["Open"][day - i] / EMA200)  # OPEN
                    curr.append(stockData["Close"][day - i] / EMA200)
                    curr.append(stockData["Volume"][day - i])

                SMA14 = SMA(prices, 14)
                MACD = ExpMovingAverage(prices, 12) - ExpMovingAverage(prices, 26)
                #print(MACD)

                curr.append(wilders_rsi(prices, 14))
                curr.append(EMA200)
                #curr.append(SMA14)
                curr.append(MACD)
                #curr.append(0)
                #print(list(modelo.predict([curr]))[0])
                if 1:#float(list(modelo.predict([curr]))[0]) == float(list(model2.predict([curr]))[0]):
                    modelOutputs.append(float(list(modelo.predict([curr]))[0]))
                    naturalOutputs.append(abs(stockData["Close"][day+1]/stockData["Open"][day+1]-1))



                    if stockData["Close"][day+1]/stockData["Open"][day+1]-1 > 0:
                        winLoss.append(1)
                    else:
                        winLoss.append(0)
                    if winLoss[-1] == modelOutputs[-1]:
                        money += money*abs(naturalOutputs[-1])
                        dubs.append(abs(stockData["Close"][day+1]/stockData["Open"][day+1]-1))
                        print("YAAAS")
                    else:
                        money -= money*abs(naturalOutputs[-1])
                        losses.append(abs(stockData["Close"][day+1]/stockData["Open"][day+1]-1))
                        pass
            prices.append(stockData['Close'][day])
        diff = 0
        #print("a", naturalOutputs)
        #print(modelOutputs)
        for i in range(len(modelOutputs)):

            if winLoss[i] != modelOutputs[i]:
                diff+=1
        #print(diff, len(modelOutputs), 1-diff/len(modelOutputs))

        finalso.append(1-diff/len(modelOutputs))
        finalsa.append(sum(naturalOutputs)/len(naturalOutputs))

print("Money: ",money)
awnser = finalso.index(max(finalso))
print(sum(losses)/len(losses), sum(dubs)/len(dubs))
print(finalso[awnser], symbols[awnser], finalsa[awnser], len(modelOutputs))
