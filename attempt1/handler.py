from attempt1.Agent import Jerry
import attempt1.Attributes
import neat
import random
import os
import pickle

Properties = attempt1.Attributes.Properties()
GroupedData = Properties.dayGroupedData()
print(len(GroupedData))
Prices = Properties.current()
Dates = Properties.times()
NumericTimes = Properties.preciseTimes()

Opens = Properties.opens()
import matplotlib.pyplot as plt


plt.ion()

class Operator():
    def __init__(self):
        self.position = 0
        self.agentsInGen = 1000



    def buyTraining(self, pickle_file):

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    'config_file.txt')

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        # p.add_reporter(neat.Checkpointer(5))

        # Run for up to 50 generations.
        winner = p.run(self.buy_fitness_func, 500)
        #print(winner.bPos2)
        # show final stats

        final_net = neat.nn.FeedForwardNetwork.create(winner, config)
        final_net.BoughtAt = 11.7795
        #pickling data

        with open(pickle_file, "wb") as file:

            pickle.dump(final_net, file)
            file.close()
        print("fajfajff", winner.fitness, winner.BoughtAt)
    def sellTraining(self, pickle_file):

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    'sell_config_file.txt')

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        # p.add_reporter(neat.Checkpointer(5))

        # Run for up to 50 generations.
        winner = p.run(self.sell_fitness_func, 500)

        # show final stats
        print("afa", winner.BoughtAt)
        final_net = neat.nn.FeedForwardNetwork.create(winner, config)
        final_net.BoughtAt = winner.BoughtAt
        #pickling data

        with open(pickle_file, "wb") as file:

            pickle.dump(final_net, file)
            file.close()
        print(winner.fitness, winner.BoughtAt)

    def local_max(self, ys):
        lis = []
        for y, i in enumerate(ys):
            if y != 0 and y != len(ys) - 1:
                if ys[y - 1] < ys[y] and ys[y + 1] < ys[y]:
                    lis.append(y)

        return lis

    def local_min(self, ys):
        lis = []
        for y, i in enumerate(ys):
            if y >= 5 and y <= len(ys) - 5:
                if ys[y - 1] > ys[y] and ys[y + 1] > ys[y] and ys[y + 2] > ys[y] and ys[y + 3] > ys[y] and ys[y + 4] > ys[y] and ys[y - 2] > ys[y] and ys[y - 3] > ys[y]:
                    lis.append(y)

        return lis
    def score_pos_min(self, pos, ys):
        bests = self.local_min(ys)
        final = []
        for curr, obj in enumerate(bests):
            if abs(obj - pos) < 4:
                return abs(obj - pos) * 5
            else:
                final.append(abs(obj - pos))

        return -min(final)*4

    def score_pos_max(self, pos, ys):
        bests = self.local_min(ys)
        final = []
        for curr, obj in enumerate(bests):
            if abs(obj - pos) < 4:
                return abs(obj - pos) * 5
            else:
                final.append(abs(obj - pos))

        return -min(final) * 4
    def sell_fitness_func(self, genomes, config):
        def BestAgent(config_path="config_file.txt"):
            config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                        neat.DefaultStagnation, config_path)
            # Unpickle saved winner
            with open('final.pickle', "rb") as f:
                genome = pickle.load(f)
                # print(genome.fitness, " genome fitness", genome.BoughtAt)
            # Convert loaded genome into required data structure

            return genome
        nets = []
        agents = []
        ge = []
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            nets.append(net)
            agents.append(Jerry())
            ge.append(genome)

            # Day Generalized Data(Same for all NN)
        mainAgent = BestAgent()
        rand = random.randint(1, 100)
        rand2 = random.randint(1, 100)
        numss = 3
        nums = [random.randint(1, len(GroupedData)-10) for i in range(numss)]
        pricesB = [GroupedData[nums[i] % len(GroupedData)] for i in range(numss-1)]
        todaysOpenB = [Opens[nums[i] % len(Opens)] for i in range(numss-1)]

        specificTimesB = [NumericTimes[nums[i] % len(NumericTimes)] for i in range(numss-1)]
        pricesB.append(GroupedData[10])
        todaysOpenB.append(Opens[10])
        specificTimesB.append(NumericTimes[10])


        # Day Generalized Data(Same for all NN)

        # Constant Parameters

        tracer = 0
        didBuyGuyBuy = False
        # Constant Parameters
        for round in range(numss):

            prices = pricesB[round]
            todaysOpen = todaysOpenB[round]
            specificTimes = specificTimesB[round]
            prev = prices[0]
            #y=-(1/390)(x-100)^2 + 100
            for i in range(len(prices)):
                currentPrice = prices[i]
                distFromOpen = todaysOpen - currentPrice
                if didBuyGuyBuy == False:
                    decision = mainAgent.activate([currentPrice, tracer, distFromOpen, .01 * specificTimes[i]])
                    if decision[0] > 0.5:
                        didBuyGuyBuy = True
                        mainAgentBoughtPos = i
                        mainAgentBoughtAt = currentPrice
                else:
                    for pos, agent in enumerate(agents):

                        if not agent.isBought:

                            decision2 = nets[agents.index(agent)].activate([currentPrice, tracer, distFromOpen, .01*specificTimes[i], mainAgentBoughtAt])
                            if decision2[0] > 0.5:

                                agent.boughtPosition = i
                                agent.bPos2 = specificTimes[i]
                                agent.BoughtAt = currentPrice
                                agent.isBought = True
                                agent.yourMom = 1
                                #print(agent.bPos2)
                if i != 0:
                    prev = prices[i - 1]
                if tracer < 0:
                    tracer = 0
                tracer += 100 * (currentPrice - prev)


            for pos, agent in enumerate(agents):

                BuyPos = .2*(-((1/60)*((agent.boughtPosition-170)**2)) + 100)


                try:

                    sellOppurtunity = (max(prices[agent.boughtPosition:agent.boughtPosition+25]) - agent.BoughtAt)
                    distanceFromLocalMin = self.score_pos_max(agent.boughtPosition, prices)
                    if agent.boughtPosition-mainAgentBoughtPos < 3:
                        ge[pos].fitness -= 20
                    ge[pos].fitness += agent.BoughtAt+distanceFromLocalMin-mainAgentBoughtAt
                    ge[pos].BoughtAt = agent.bPos2

                    if agent.bPos2 <= 650 or agent.isBought == False:
                        ge[pos].fitness -= 1000
                    else:
                        pass
                except:

                    ge[pos].fitness -= 10000000000000

            #print("Stuff: ", BuyPos, BoughtFitness, buyBeforeHigh, ge[pos].fitness, agent.boughtPosition)




        for pos, agent in enumerate(agents):
            ge.pop(pos)
            nets.pop(pos)
            agents.pop(pos)




        self.position += 1


    def buy_fitness_func(self, genomes, config):

        nets = []
        agents = []
        ge = []
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            nets.append(net)
            agents.append(Jerry())
            ge.append(genome)

            # Day Generalized Data(Same for all NN)

        rand = random.randint(1, 100)
        rand2 = random.randint(1, 100)
        numss = 4
        nums = [random.randint(1, len(GroupedData)-10) for i in range(numss)]
        pricesB = [GroupedData[nums[i] % len(GroupedData)] for i in range(numss - 1)]
        todaysOpenB = [Opens[nums[i] % len(Opens)] for i in range(numss - 1)]

        specificTimesB = [NumericTimes[nums[i] % len(NumericTimes)] for i in range(numss - 1)]



        # Day Generalized Data(Same for all NN)

        # Constant Parameters

        tracer = 0
        # Constant Parameters
        for round in range(numss-1):

            prices = pricesB[round]
            todaysOpen = todaysOpenB[round]
            specificTimes = specificTimesB[round]
            prev = prices[0]
            #y=-(1/390)(x-100)^2 + 100
            for i in range(len(prices)):
                currentPrice = prices[i]
                distFromOpen = todaysOpen - currentPrice

                for pos, agent in enumerate(agents):

                    if not agent.isBought:

                        decision = nets[agents.index(agent)].activate([currentPrice, tracer, distFromOpen, .01*specificTimes[i]])
                        if decision[0] > 0.5:
                            agent.boughtPosition = i
                            agent.bPos2 = specificTimes[i]
                            agent.BoughtAt = currentPrice
                            agent.isBought = True
                if i != 0:
                    prev = prices[i - 1]
                if tracer < 0:
                    tracer = 0
                tracer += 100 * (currentPrice - prev)


            for pos, agent in enumerate(agents):

                BuyPos = .2*(-((1/15)*((agent.boughtPosition-100)**2)) + 100)



                try:

                    sellOppurtunity = (max(prices[agent.boughtPosition:]) - agent.BoughtAt)
                    distanceFromLocalMin = self.score_pos_min(agent.boughtPosition, prices)
                    ge[pos].fitness += sellOppurtunity + distanceFromLocalMin
                    ge[pos].BoughtAt = agent.bPos2

                    if agent.bPos2 <= 638 or agent.isBought == False:
                        ge[pos].fitness -= 1000
                    else:
                        pass
                except:
                    ge[pos].fitness -= 10000000000000

            #print("Stuff: ", BuyPos, BoughtFitness, buyBeforeHigh, ge[pos].fitness, agent.boughtPosition)




        for pos, agent in enumerate(agents):
            ge.pop(pos)
            nets.pop(pos)
            agents.pop(pos)




        self.position += 1


if __name__ == '__main__':

    operator = Operator()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    operator.buyTraining('final.pickle')
    operator.sellTraining('sell2.pickle')