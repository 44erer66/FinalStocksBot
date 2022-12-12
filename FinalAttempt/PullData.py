from datetime import datetime
import yfinance as yf

def refresh_data(sym):
    for symbol in [sym]:
        print(symbol)
        #start_date = datetime(2015, 10, 10)
        start_date = datetime(2019, 5, 6)
        end_date = datetime(2030, 10, 6)

        # get the data
        data = yf.download(symbol, start=start_date,
                           end=end_date)

        data.to_csv("/Users/44erer66/Desktop/StockBot/TestingData/"+symbol+".csv")

