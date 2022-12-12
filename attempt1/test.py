from matplotlib import pyplot as plt
from attempt1.Agent import Jerry
from attempt1.Attributes import Properties
import neat
import pickle


pricesF = Properties().dayGroupedData()
times = Properties().preciseTimes()
opens = Properties().opens()

def BestAgent(config_path="config_file.txt"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    # Unpickle saved winner
    with open('final.pickle', "rb") as f:
        genome = pickle.load(f)
        #print(genome.fitness, " genome fitness", genome.BoughtAt)
    # Convert loaded genome into required data structure
    print(genome.BoughtAt)
    return genome
def BestAgent2(config_path="sell_config_file.txt"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    # Unpickle saved winner
    with open('sell2.pickle', "rb") as f:
        genome = pickle.load(f)

    print(genome.BoughtAt, "gg")
    return genome
ourPrices = [500]
solds = []
currentTotal = 500
startingPrice = 500
totalProfit = 0
genome = BestAgent()
genome2 = BestAgent2()

print(pricesF[9])
for day in range(len(pricesF)):
    prices = pricesF[day]
    todaysOpen = opens[day]
    agent = Jerry()
    prev = prices[0]
    tracer = 0

    # y=-(1/390)(x-100)^2 + 100
    for i in range(len(prices)):
        currentPrice = prices[i]
        distFromOpen = todaysOpen - currentPrice

        currentTime = times[day][i]

        if not agent.isBought:

            decision = genome.activate([currentPrice, tracer, distFromOpen, .01 * currentTime])
            if decision[0] > 0.5:
                agent.boughtPosition = i
                agent.bPos2 = currentTime
                agent.BoughtAt = currentPrice
                agent.isBought = True

        else:
            decision2 = genome2.activate([currentPrice, tracer, distFromOpen, .01 * currentTime, agent.BoughtAt])
            if decision2[0] > 0.5:
                agent.sellPosition = i
                agent.SoldAt = currentPrice
                break
        if i != 0:
            prev = prices[i - 1]
        if tracer < 0:
            tracer = 0
        tracer += 100 * (currentPrice - prev)
    if agent.SoldAt == 0 and agent.BoughtAt != 0:
        agent.SoldAt = prices[-1]
    try:
        totalProfit = (agent.SoldAt-agent.BoughtAt)*(currentTotal/agent.BoughtAt)
    except:
        totalProfit =0
    print("gg", totalProfit, agent.BoughtAt, agent.SoldAt, currentTotal)
    currentTotal += totalProfit
    ourPrices.append(currentTotal)
    solds.append((agent.SoldAt, agent.BoughtAt))





print(totalProfit, currentTotal, startingPrice)
print(ourPrices)
print(solds)
plt.plot(ourPrices)



plt.show()