import pandas as pd
import yfinance as yf
import pickle
import datetime
from termcolor import colored


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
        return [0][0]
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

with open('MinuteData/buyAgent.pickle', "rb") as f:
    model = pickle.load(f)
with open('MinuteData/sellAgent.pickle', "rb") as f:
    model2 = pickle.load(f)

def get_stocks():
    # with open('Agent2.pickle', "rb") as f:
    # model = pickle.load(f)
    data2 = pd.read_csv('S&P500.csv')
    symbols = list(data2["Symbol"])

    total = 500
    prices = []

    outputs = []
    modelOutputs = []
    testing = []
    for pos, symbol in enumerate(symbols):

        with open("Agents/" + symbol + ".pickle", "rb") as f:
        #with open("Agent2.pickle", "rb") as f:
            modelo = pickle.load(f)

        stockData = pd.read_csv("StocksData/" + symbol + ".csv")
        #testingData = pd.read_csv("TestingData/"+ symbol + ".csv")
        day = len(stockData["Close"])  # 321
        # print(day, len(stockData["High"]))
        try:
            curr = []
            curro = []
            #actualVariance = testingData["Close"][0] / testingData["Open"][0]-1
            for i in range(1, 15):
                # print(len(stockData["High"]), symbol)
                curr.append(stockData["High"][day - i])  # HIGH
                curr.append(stockData["Low"][day - i])  # LOW
                curr.append(stockData["Open"][day - i])  # OPEN
                curr.append(stockData["Close"][day - i])
                curr.append(stockData["Volume"][day - i])
                curr.append(stockData["Adj Close"][day - i])

            days10 = stockData["Close"][day - 1] - stockData["Close"][day - 10]
            days20 = stockData["Close"][day - 1] - stockData["Close"][day - 20]
            days50 = stockData["Close"][day - 1] - stockData["Close"][day - 50]
            days100 = stockData["Close"][day - 1] - stockData["Close"][day - 100]
            #print(list(stockData['Close']))
            curr.append(SMA(stockData['Close'], 8))
            curr.append(SMA(stockData['Close'], 10))
            curr.append(SMA(stockData['Close'], 20))
            curr.append(SMA(stockData['Close'], 50))
            curr.append(SMA(stockData['Close'], 100))
            #curr.append(RSI(stockData['Close']))
            curr.append(SO(stockData['Close']))
            curr.append(WR(stockData['Close']))
            #print(curr)
            # print(model.predict([curr]))
            modelOutputs.append(modelo.predict([curr]))
            #outputs.append(actualVariance)
            # testing.append(model.predict([curr])-actualVariance)
            #print(modelo.predict([curr]), symbol)
        except:
            modelOutputs.append(0)
            outputs.append(0)

    chosenSymbol = symbols[modelOutputs.index(max(modelOutputs))]

    chosenVariance = modelOutputs[modelOutputs.index(max(modelOutputs))]

    # print("Margin" + str(sum(testing)/len(testing)))
    print(chosenVariance, "l")

    #plt.plot(final1)
    #plt.plot(final2)
    #print(counter/len(modelOutputs))
    #plt.show()
    print(chosenSymbol)
    return [chosenSymbol, chosenVariance]



def getStockAmmount(symbol, cost):
    money = 2200
    cost = int(cost)

    return int(money // cost)


def buyStock(symbol, amt):
    api.submit_order(symbol=symbol,
                     qty=amt,
                     side="buy",
                     type="market",
                     time_in_force="day")


def sellStock(symbol, amt):
    api.submit_order(symbol=symbol,
                     qty=amt,
                     side="sell",
                     type="market",
                     time_in_force="day")

def parsePrice(symbol, prev):
    while True:
        try:
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            return todays_data['Close'][0]

        except:
            return prev

symbol = get_stocks()[0]
predictedVariance = get_stocks()[1]
print(symbol)
#[-0.12387255]
key = "AKH3R964QCZO3M4XMHTL"
sec = "Gmxy44G6Q0EpagU5ndARSNdwmVZzBtOflxNmxbou"
url = "https://api.alpaca.markets"
api = tradeapi.REST(key, sec, url, api_version='v2')
account = api.get_account()



print(colored("Starting algorithm to get the best stock.", "green"))
print(colored("Found Stock: " + symbol))
print(colored("YAAS QUEEN", "green"))

csp = 0

data = pd.read_csv("TestData.csv")



isBought = False


run = True
start = False
limitVariance = 100
sellPos = 0
soldAt = (0, 0)
ammount = 0
BoughtAt = 0
Open = 0
isRun = False
prices = [59.59]

currPrice = 0
currentTime = 0

while run:

    h, m = int(datetime.datetime.now().strftime("%H")), int(datetime.datetime.now().strftime("%M"))

    if not start:

        if h > 5 and h < 16 and m > 29:
            try:
                start = True
                Open = parsePrice(symbol, 0)
                ammount = getStockAmmount(symbol, parsePrice(symbol, 0))
                buyStock(symbol, ammount)
                print("starting")
                prices.append(Open)
                currentTime = h*100+m
            except:
                pass
    if start:

        currPrice = parsePrice(symbol, 0)
        currVariance = currPrice/Open - 1

        if currVariance > 0.0083:
          sellStock(symbol, ammount)
          print("we sold the stock")

        if h == 12 and m == 58:
            sellStock(symbol, ammount)
        prices.append(currPrice)

print(prices)