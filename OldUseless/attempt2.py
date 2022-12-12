
import pandas as pd
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import pickle
# Import the Height Weight Dataset

data = pd.read_csv('salaries.csv')
data2 = pd.read_csv('../S&P500.csv')
print(list(data2['Symbol']))
#symbols = list(data2["Symbol"])



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



def get_model():
    import pandas as pd
    symbols = list(data2["Symbol"])
    for io in range(len(data["Gender"])):
        if data["Gender"][io] == "Male":
            data["Gender"][io] = 1
        else:
            data["Gender"][io] = 0

    inputs = []
    outputs = []
    for pos, symbol in enumerate(symbols):

        stockData = pd.read_csv('StocksData/'+symbol+".csv")

        for day in range(len(stockData["High"])):
            if day >101:
                curr = []
                curro = []
                curro.append(stockData["Close"][day]/stockData["Open"][day]-1)
                for i in range(1, 25):

                    curr.append(stockData["High"][day-i])#HIGH
                    curr.append(stockData["Low"][day-i])#LOW
                    curr.append(stockData["Open"][day-i])#OPEN
                    curr.append(stockData["Close"][day-i])
                    curr.append(stockData["Volume"][day-i])
                    curr.append(stockData["Adj Close"][day-i])

                days10 = stockData["Close"][day-1] - stockData["Close"][day-10]
                days20 = stockData["Close"][day-1] - stockData["Close"][day-20]
                days50 = stockData["Close"][day-1] - stockData["Close"][day-50]
                days100 = stockData["Close"][day-1] - stockData["Close"][day-100]
                curr.append(days10)
                curr.append(days20)
                curr.append(days50)
                curr.append(days100)

                send = True
                for i in curr:
                    try:
                        if i == int(i):
                            pass
                    except:
                        send = False
                        print(i)
                for i in curro:
                    try:
                        if i == int(i):
                            pass
                    except:
                        send = False
                        print(i)
                if send:
                    inputs.append(curr)
                    outputs.append(curro)
    import pandas as pd

    # There are 2 tables on the Wikipedia page
    # we want the first table


    # Store the data in the form of dependent and independent variables separately
    print("DONE")
    X = inputs
    y = outputs
    print(len(X))
    print(len(y))
    # In[3]:

    # Split the Dataset into Training and Test Dataset
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # In[5]:


    # Import the Decision Tree Regressor
    from sklearn.tree import DecisionTreeRegressor

    # Create a decision tree regressor object  from DecisionTreeRegressor class
    DtReg = DecisionTreeRegressor(random_state=0)

    # Fit the decision tree regressor with training data represented by X_train and y_train

    print(len(X_train))
    print(len(y_train))

    DtReg.fit(X_train, y_train)

    with open("../Agent2.pickle", "wb") as file:

        pickle.dump(DtReg, file)
        file.close()
    # In[7]:
    return DtReg

model = get_model()
symbols = ["CODX"]

inputs = []
outputs = []
modelOutputs = []
"""
for pos, symbol in enumerate(symbols):

    stockData = pd.read_csv(symbol+".csv")

    for day in range(len(stockData["High"])):
        if day > 101:
            curr = []
            curro = []
            curro.append(1-stockData["Close"][day]/stockData["Open"][day])
            for i in range(1, 6):

                curr.append(stockData["High"][day-i])#HIGH
                curr.append(stockData["Low"][day-i])#LOW
                curr.append(stockData["Open"][day-i])#OPEN
                curr.append(stockData["Close"][day-i])
                curr.append(stockData["Volume"][day-i])
                curr.append(stockData["Adj Close"][day-i])

            days10 = stockData["Close"][day] - stockData["Close"][day-10]
            days20 = stockData["Close"][day] - stockData["Close"][day-20]
            days50 = stockData["Close"][day] - stockData["Close"][day-50]
            days100 = stockData["Close"][day] - stockData["Close"][day-100]
            curr.append(days10)
            curr.append(days20)
            curr.append(days50)
            curr.append(days100)
            print(model.predict([curr]), curr)
            modelOutputs.append(model.predict([curr]))
            inputs.append(curr)
            outputs.append(curro)
plt.plot(modelOutputs)
plt.plot(outputs)
plt.show()
"""