import ta

import pandas as pd
import pickle
"""
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=1min&apikey=MHZ7HTHFSKVMCP8B'
r = requests.get(url)
data = r.json()
print(data)
#df = pd.read_json(data)
#df.to_csv()
#print(df)
"""


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
import numpy as np
def ExpMovingAverage(values, window):
    try:
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()

        a = np.convolve(values, weights)[:len(values)]
        a[:window] = a[window]
        return a[-1]
    except:
        return 1/0

def get_model():

    inputs = []
    outputs = []
    dfs = ['Binance_ETHUSDT_2021_minute.csv', 'Binance_LTCUSDT_2022_minute.csv', 'Binance_TRXUSDT_2021_minute.csv', 'Binance_TRXUSDT_2022_minute.csv']
    for dataframe in dfs:
        df = pd.read_csv(dataframe)
        print(len(df['open']))
        prices = list(df['open'])[::-1][::10]
        for pos, price in enumerate(prices):

            try:
                pastPrices = list(prices)[:pos+1]
                #print(pastPrices)
                addedInputs = []
                addedOutputs = []
                MACD = ExpMovingAverage(prices, 12) - ExpMovingAverage(prices, 26)
                #RSI, SMA(8,14), SO, WR
                addedInputs.append(RSI(pastPrices)[0])
                addedInputs.append(ExpMovingAverage(pastPrices, 200))
                addedInputs.append(MACD)
                for i in range(1, 10):
                    addedInputs.append(prices[pos-i]/ExpMovingAverage(pastPrices, 200))
                #Output 1 or 0 based on if next price is up or down because we are trying to short

                x = 0
                adder = -1
                for i in prices[pos:]:
                    x+=1
                    if i > price*1.02:
                        #addedOutputs.append(x)
                        adder = x
                        break
                    if i < price*0.99:
                        #addedOutputs.append(0)
                        adder = 0
                        break
                if adder == -1:
                    print(1/0)
                addedOutputs.append(adder)

                #print(addedOutputs)
                #print(addedInputs)
                inputs.append(addedInputs)
                outputs.append(addedOutputs)
                #print("DUB")
            except:
                print("FAIL")





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
    print(X_train)
    print(y_train)
    #print(y_train)
    DtReg.fit(X_train, y_train)

    with open("Crypto.pickle", "wb") as file:
        pickle.dump(DtReg, file)
        file.close()
    # In[7]:
    return DtReg
get_model()