from attempt1.get_stock_prices import parsePrice
import alpaca_trade_api as tradeapi
import datetime
from termcolor import colored
from attempt1.Agent import Jerry
import neat
import pickle

key = "AKH3R964QCZO3M4XMHTL"
sec = "Gmxy44G6Q0EpagU5ndARSNdwmVZzBtOflxNmxbou"
url = "https://api.alpaca.markets"
api = tradeapi.REST(key, sec, url, api_version='v2')
account = api.get_account()


def getStockAmmount(symbol, cost):
    money = int(float(account.cash)) * .75
    cost = int(cost)

    return int(money // cost) - 1


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


def BestAgent(file, config_path="config_file.txt"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    # Unpickle saved winner
    with open(file, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    completed_genome = genome
    net = neat.nn.FeedForwardNetwork.create(completed_genome, config)
    return net

if __name__ == '__main__':

    print(account.cash)

    print(colored("Starting algorithm to get the best stock.", "green"))
    symbol = "BTBT"
    prevcsp = parsePrice(symbol, 0)
    print(colored("Found Stock: " + symbol + ", with current price: " + str(prevcsp), "green"))
    print(colored("YAAS QUEEN", "green"))

    csp = 0
    BoughtAt = None
    SoldAt = None

    tracer = 0.00

    Open = parsePrice(symbol, 0)
    amount = 1

    isBought = False
    prevcsp = parsePrice(symbol, 0)

    run = True
    start = False

    genome = BestAgent('genome.pickle')
    sGenome = BestAgent('sell2.pickle', config_path='sell_config_file.txt')
    mainAgent = Jerry()
    while run:
        h, m = int(datetime.datetime.now().strftime("%H")), int(datetime.datetime.now().strftime("%M"))
        if h > 5 and h < 16 and m > 28:
            start = True
            # print("starting")
        if start:
            csp = parsePrice(symbol, prevcsp)
            Open = Open
            h, m = int(datetime.datetime.now().strftime("%H")), int(datetime.datetime.now().strftime("%M"))
            fTime = h*100 + m*1

            if not mainAgent.isBought:

                if genome.activate([csp, tracer, Open - csp, fTime])[0] > 0.5:

                    mainAgent.BoughtAt = csp
                    mainAgent.isBought = True
                    buyStock(symbol, amount)
                    print('I have bought the stock at price ', csp, 'and it is bought at ', h, ':', m)
                else:
                    pass
            else:
                if sGenome.activate([csp, tracer, Open - csp, fTime, BoughtAt])[0] > 0.5:

                    mainAgent.SoldAt = csp

                    sellStock(symbol, amount)
                    print('I have bought the stock at price ', csp, 'and it is bought at ', h, ':', m)
                    run = True
                else:
                    pass


            if not mainAgent.isBought:
                if tracer < 0:
                    tracer = 0
            else:
                if tracer < 0:
                    tracer = 0

            tracer += 100 * (csp - prevcsp)

            prevcsp = csp