import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def ExpMovingAverage(values, window):
    try:
        weights = np.exp(np.linspace(-1.,0.,window))
        weights /= weights.sum()

        a = np.convolve(values, weights)[:len(values)]
        a[:window] = a[window]
        return a
    except:
        return 0

df = pd.read_csv('test.csv')
prices = list(df['open'])[::15]

exp26 = ExpMovingAverage(prices, 26)
exp12 = ExpMovingAverage(prices, 12)

section1x = []
section1y = []
section2x = []
section2y= []

ticker = False
distance = 0
for i in range(len(prices)):

    try:
        if exp12[i-1] <= exp26[i] and exp26[i] <= exp12[i+1] or exp26[i-1] <= exp12[i] and exp12[i] <= exp26[i+1]\
                and exp12[i-1] >=  exp26[i] and exp26[i] >= exp12[i+1] or exp26[i-1] >= exp12[i] and exp12[i] >= exp26[i+1]:
            if distance > 1:
                if ticker:
                    section2x.append(i)
                    section2y.append(prices[i])
                else:
                    section1x.append(i)
                    section1y.append(prices[i])

                ticker = not ticker
                distance = 0
    except:
        pass
    distance += 1

#print(section1x)
plt.plot(prices)
plt.plot(exp12)
plt.plot(exp26)
plt.scatter(section2x, section2y)
plt.scatter(section1x, section1y)
plt.show()