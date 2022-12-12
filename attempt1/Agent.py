
import random
import math



class Jerry():
    def __init__(self):

        #Day Generalized Data(Same for all NN)

        #Day Generalized Data(Same for all NN)

        #Data used to grade the Agent
        self.isBought = False
        self.BoughtAt = 0
        self.score = 0
        self.SoldAt = 0
        self.boughtPosition, self.soldPosition = 0, -50
        self.boughtTime = 0
        self.yourMom = 2
        self.bPos2 = 'YO'
        #Data used to grade the Agent

        #Constant Parameters

        self.tracer = 0
        #Constant Parameters

    def buy(self, price):
        self.BoughtAt = price
        self.isBought = True
    def sell(self, price):
        if self.isBought:
            self.SoldAt = price


