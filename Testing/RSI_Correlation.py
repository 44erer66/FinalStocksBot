from matplotlib import pyplot as plt
import pandas as pd
import typing
import numpy as np
def calculate_rsi(prices, n):
    """Calculate the relative strength index (RSI) for a list of prices.

    Arguments:
    prices -- a list of prices
    n -- the number of periods to use in the calculation (default 14)

    Returns:
    A list of RSI values, with the same length as the input list.
    """
    # Calculate the differences between successive elements in the list
    diffs = [prices[i+1] - prices[i] for i in range(len(prices)-1)]

    # Initialize the list of gains and losses with the first n-1 elements
    # set to zero (since we don't have enough data yet to calculate RSI)
    gains = [0] * (n-1)
    losses = [0] * (n-1)

    # Iterate through the differences and populate the gains and losses lists
    for i in range(n-1, len(diffs)):
        if diffs[i] > 0:
            gains.append(diffs[i])
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-diffs[i])

    # Calculate the averages of the gains and losses
    avg_gain = sum(gains[-n:]) / n
    avg_loss = sum(losses[-n:]) / n

    # Initialize the list of RSIs with the first n-1 elements set to zero
    rsis = [0] * (n-1)

    # Iterate through the gains and losses and calculate the RSI
    for i in range(n-1, len(gains)):
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        rsis.append(rsi)

    return int(rsis[-1])
def EMA(values, window):
    try:
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()

        a = np.convolve(values, weights)[:len(values)]
        a[:window] = a[window]
        return a[-1]
    except:
        return 1/0
stockData = list(pd.read_csv('/Users/44erer66/PycharmProjects/FinalStocksBot/StocksData/AAPL.csv')['Close'])

elements = []
prices = []
elements2 = []
print(len(stockData))
score = 0
score2 = 0
for i in range(2000):
    prices.append(stockData[i])
    if i > 26:
        elem1 = stockData[i + 1] / stockData[i] - 1
        if elem1 < 0:

            elem2 = EMA(prices, 26) - EMA(prices, 12)
            if elem2 > 0:
                score+=1
            elements.append((elem1, elem2))
        if elem1 > 0:

            elem2 = EMA(prices, 26) - EMA(prices, 12)
            if elem2>0:
                score2 += 1

            elements2.append((elem1, elem2))

elements.sort(key=lambda y: y[1])
elements2.sort(key = lambda y: y[1])
print(score, score2)
x = []
y = []
for i in elements:
    x.append(i[0])
    y.append(i[1])
x2 = []
y2 = []
for i in elements2:
    x2.append(i[0])
    y2.append(i[1])
print(len(x), len(y))
plt.scatter(y, x)
plt.scatter(y2,x2)
plt.show()
