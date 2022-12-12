import yfinance as yf
def parsePrice(symbol, prev):
    while True:
        try:
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            return todays_data['Close'][0]

        except:
            return prev
