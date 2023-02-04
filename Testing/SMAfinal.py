from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import alpaca_trade_api as tradeapi
key = "AKH3R964QCZO3M4XMHTL"
sec = "Gmxy44G6Q0EpagU5ndARSNdwmVZzBtOflxNmxbou"
url = "https://api.alpaca.markets"
api = tradeapi.REST(key, sec, url, api_version='v2')
account = api.get_account()

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

def parsePrice(symbol):
    while True:
        try:
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            return todays_data['Close'][0]

        except:
            return False
def refresh_data(sym):
    for symbol in [sym]:
        print(symbol)
        #start_date = datetime(2015, 10, 10)

        start_date = datetime.today() - timedelta(days=14)
        end_date = datetime.today()

        # get the data
        data = yf.download(symbol, start=start_date,
                           end=end_date)

        data.to_csv("/Users/44erer66/PycharmProjects/FinalStocksBot/Testing/"+symbol+".csv")
def SMA2(numbers, window_size):
  moving_averages = []
  for i in range(len(numbers) - window_size + 1):
    window = numbers[i:i + window_size]
    moving_averages.append(sum(window) / len(window))
  return moving_averages[-1]
def ReturnAdjustedSMA(lis, value):
    return SMA2(lis.append(value), 7)
def main(lookBack):#CurrentPosition(Bought, Shorted, or None)
    CurrentPosition = None#CurrentPosition(Bought, Shorted, or None)
    run = True
    while run:
        refresh = 0  # Have we refreshed the data
        now = datetime.now()
        current_hour = int(now.strftime("%H"))
        if not refresh and current_hour == 6:
            refresh_data('TQQQ')
            refresh += 1
            prices = pd.read_csv('/Users/44erer66/PycharmProjects/FinalStocksBot/Testing/TQQQ.csv')['Close']
            oldSMA = SMA2(prices, 7)
            pastSMA = [oldSMA]
        if refresh and current_hour == 13:
            refresh -= 1


        if refresh:
            currentPrice = parsePrice('TQQQ')
            if currentPrice != False:
                currentSMA = ReturnAdjustedSMA(prices, currentPrice)
                pastSMA.append(currentSMA)
                if CurrentPosition == True:#Have a Bought Position Open
                    if pastSMA[0] >= currentPrice and pastSMA[1] < currentPrice: #The price has intersected from above
                        ammount = (account.cash*1.5)/currentPrice
                        sell_stock('TQQQ', ammount)#Sell First Time
                        sell_stock('TQQQ', ammount)#Short


                if CurrentPosition == False:#Have a Shorted Position Open
                    if pastSMA[0] <= currentPrice and pastSMA[1] > currentPrice: # The price has intersected from below
                        ammount = (account.cash * 1.5) / currentPrice
                        buy_stock('TQQQ', ammount)  # Sell First Time
                        buy_stock('TQQQ', ammount)  # Short
                if CurrentPosition == None:# Have no Position Open
                    ammount = (account.cash * 1.5) / currentPrice
                    if pastSMA[0] <= currentPrice and pastSMA[1] > currentPrice:
                        buy_stock('TQQQ', ammount)
                    if pastSMA[0] >= currentPrice and pastSMA[1] < currentPrice:
                        sell_stock('TQQQ', ammount)
                pastSMA.pop(0)