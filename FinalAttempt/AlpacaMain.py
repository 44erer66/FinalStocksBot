#IMPORTS
#final
import numpy as np
import pickle
import pandas as pd
import typing
import alpaca_trade_api as tradeapi
from termcolor import colored
from attempt3 import get_model
from PullData import refresh_data
import yfinance as yf
key = "AKH3R964QCZO3M4XMHTL"
sec = "Gmxy44G6Q0EpagU5ndARSNdwmVZzBtOflxNmxbou"
url = "https://api.alpaca.markets"
api = tradeapi.REST(key, sec, url, api_version='v2')
account = api.get_account()
def parsePrice(symbol, prev):
    while True:
        try:
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            return todays_data['Close'][0]

        except:
            return prev
#STOCK ANALYSIS FUNCTIONS
def wilders_rsi(data: list, window_length: int, use_rounding: bool = True) -> typing.List[typing.Any]:
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
def ExpMovingAverage(values, window):
    try:
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()

        a = np.convolve(values, weights)[:len(values)]
        a[:window] = a[window]
        return a[-1]
    except:
        return 1/0
#STOCK ANALYSIS FUNCTION

def make_prediction(sym):
    symbol = sym

    refresh_data(sym)



    stockData = pd.read_csv('/Users/44erer66/PycharmProjects/FinalStocksBot/TestingData/'+symbol+'.csv')
    with open("/Users/44erer66/PycharmProjects/FinalStocksBot/Agents/"+symbol+".pickle", "rb") as f:
        model = pickle.load(f)
    prices = list(stockData["Close"])
    day = len(prices)-1
    curr = []
    EMA200 = ExpMovingAverage(prices, 200)
    for i in range(0, 8):
        # curr.append(stockData["High"][day - i] / EMA200)  # HIGH
        # curr.append(stockData["Low"][day - i] / EMA200)  # LOW
        # curr.append(stockData["Open"][day - i] / EMA200)  # OPEN
        curr.append(list(stockData["Close"])[day - i] / EMA200)
        curr.append(list(stockData["Volume"])[day - i])
    SMA14 = SMA(prices, 14)
    MACD = ExpMovingAverage(prices, 12) - ExpMovingAverage(prices, 26)
    curr.append(wilders_rsi(prices, 14))
    curr.append(EMA200)
    # curr.append(SMA14)
    curr.append(MACD)

    prediction = model.predict([curr])[0]

    print(prediction)
    return prediction

from datetime import datetime

def buy_stock(symbol, amt):
    api.submit_order(symbol=symbol,
                     qty=amt,
                     side="buy",
                     type="market",
                     time_in_force="day")


def sell_stock(symbol, amt):
    api.submit_order(symbol=symbol,
                     qty=amt,
                     side="sell",
                     type="market",
                     time_in_force="day")

def run_day():
    dt = datetime.now()
    day = int(dt.weekday())
    print(day)
    if day == 0 or day == 1 or day == 2 or day == 6:
        prediction = make_prediction('AAPL')
        print(prediction)
        run = True
        BoughtAt = 0
        plsmins = 0
        while run:
            now = datetime.now()
            current_hour = int(now.strftime("%H"))
            current_minute = int(now.strftime("%M"))
            #print(current_hour, current_minute)

            if current_hour == 6 and current_minute > 30:
                if prediction == 1:
                    buy_stock('AAPL', 30)
                    BoughtAt = parsePrice('AAPL', 0)
                    plsmins = 1
                    print('We Bought At', BoughtAt)


                else:
                    sell_stock('AAPL', 30)
                    BoughtAt = parsePrice('AAPL', 0)
                    plsmins = 0
                    print('We Bought At', BoughtAt)
                    pass
                print(colored("WE BOUGHT THE STOCK!!", 'green'))
                run = False
        run2 = True
        while run2:
            currPrice = parsePrice('AAPL', BoughtAt)
            now = datetime.now()
            current_hour = int(now.strftime("%H"))
            current_minute = int(now.strftime("%M"))
            if plsmins == 1:
                if currPrice < BoughtAt*0.98:
                    sell_stock('AAPL', 30)
                    print('WE SOLD EARLY AT', currPrice)
                    break
            else:
                if currPrice > BoughtAt * 1.02:
                    buy_stock('AAPL', 30)
                    print('WE SOLD EARLY AT', currPrice)
                    break

            if current_minute == 0:
                print(current_hour, current_minute)
            if current_hour == 12 and current_minute >= 57:
                print("ITS TIME")
                if prediction == 1:
                    sell_stock('AAPL', 30)
                    pass
                else:
                    buy_stock('AAPL', 30)
                    pass
                print(colored('WE SOLD THE STOCK!!', 'green'))
                run2 = False

        return colored('This Day was a Success','green')
    else:
        return colored('Today we did not run','yellow')
def main():
    print(colored('Initializing ...', 'green'))
    while True:
        now = datetime.now()

        current_hour = int(now.strftime("%H"))
        current_min = int(now.strftime("%M"))

        x = run_day()
        print(x)
main()