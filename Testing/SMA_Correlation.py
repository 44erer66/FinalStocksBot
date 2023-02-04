import pandas as pd
from matplotlib import pyplot as plt
def SMA(prices, lookBack):
    daySMA = []
    pos = len(prices) - 1
    if pos < lookBack:
        daySMA.append(0)
    else:
        daySMA.append(sum(prices[pos - lookBack:pos + 1]) / lookBack)
    return daySMA[0]
def SMA2(numbers, window_size):
  moving_averages = []
  for i in range(len(numbers) - window_size + 1):
    window = numbers[i:i + window_size]
    moving_averages.append(sum(window) / len(window))
  return moving_averages[-1]

def intersection(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    m = (y2 - y1) / (x2 - x1)
    b = y1-m*x1
    return (m, b)
#x = (b2-b1)/(m1-m2)
def full_intersection(point1, point2, point3, point4):
    m1, b1 = intersection(point1, point2)
    m2, b2 = intersection(point3, point4)
    x = (b2-b1)/(m1-m2)
    y = m1*x + b1
    return (x, y)

stockData = list(pd.read_csv('/Users/44erer66/PycharmProjects/FinalStocksBot/TestingData/TQQQ.csv')['Close'])[927-50:927]
prices = []
elements = []
for i in range(len(stockData)):
    price = stockData[i]

    if i > 8:
        elements.append(SMA2(prices, 7))
    prices.append(price)


stockData = stockData[9:]
valuesx1 = []
valuesy1 = []
valuesx2 = []
valuesy2 = []

isBought, isShort = False, False

profits = []
losses = []

points = []
pPoints = []
lPoints = []
wcounter = 0
lcounter = 0
for i in range(len(elements)):
    if i > 0:
        sData = stockData[i]
        SMA = elements[i]
        SMA2 = elements[i-1]
        sData2 = stockData[i-1]
        if elements[i-1] - stockData[i-1] == abs(elements[i-1] - stockData[i-1]):# Low To high/ BUY
            run = True
        else: # High To Low/ SHORT
            run = False
        if run == True and elements[i] - stockData[i] != abs(elements[i] - stockData[i]):

            x, y = i, sData#full_intersection((i-1, sData2), (i, sData), (i-1, SMA2), (i, SMA))
            if isShort == True:

                points[-1].append(x)
                points[-1].append(y)
                isShort = False
                if points[-1][1] > points[-1][3]:
                    pPoints.append(points[-1])
                    profits.append(abs((points[-1][1]-points[-1][3])/points[-1][1]))
                    wcounter+=1
                else:
                    lPoints.append(points[-1])
                    losses.append(abs((points[-1][1]-points[-1][3])/points[-1][1]))
                    lcounter+=1

            #if isShort == False:

            points.append([x, y])
            isBought = True

            valuesx1.append(x)
            valuesy1.append(y)
        if run == False and  elements[i] - stockData[i] == abs(elements[i] - stockData[i]):
            x, y = i, sData#full_intersection((i - 1, sData2), (i, sData), (i - 1, SMA2), (i, SMA))

            if isBought == True:
                points[-1].append(x)
                points[-1].append(y)
                isBought = False
                if points[-1][1] < points[-1][3]:
                    pPoints.append(points[-1])
                    profits.append(abs((points[-1][1] - points[-1][3]) / points[-1][1]))
                    wcounter += 1
                else:
                    lPoints.append(points[-1])
                    losses.append(abs((points[-1][1] - points[-1][3]) / points[-1][1]))
                    lcounter += 1

            #if isBought == False:
            points.append([x, y])
            isShort = True

            valuesx2.append(x)
            valuesy2.append(y)

print("Win Ratio:", len(profits)/(len(profits)+len(losses)))
print("Win Rate:", sum(profits)/len(profits))
print("Loss Rate:", sum(losses)/len(losses))
print(wcounter, lcounter)
for i in pPoints:
    xa1,ya1,xa2,ya2 = i
    if xa1 > xa2:
        x1 = xa2
        y1 = ya2
        x2 = xa1
        y2 = ya1
        print(x1, y1, x2, y2)
    else:
        x1, y1, x2, y2 = xa1,ya1,xa2,ya2

    xVals = [i for i in range(int(x1), int(x2)+1)]

    plt.fill_between(xVals, stockData[int(x1):int(x2)+1], elements[int(x1):int(x2)+1], alpha=0.35, color = 'green')

for i in lPoints:
    xa1, ya1, xa2, ya2 = i
    if xa1 > xa2:
        x1 = xa2
        y1 = ya2
        x2 = xa1
        y2 = ya1
        print(x1, y1, x2, y2)
    else:
        x1, y1, x2, y2 = xa1, ya1, xa2, ya2
    xVals = [i for i in range(int(x1), int(x2) + 1)]

    plt.fill_between(xVals, stockData[int(x1):int(x2) + 1], elements[int(x1):int(x2) + 1], alpha=0.35, color='red')

plt.scatter(valuesx1, valuesy1)
plt.scatter(valuesx2, valuesy2)
finalX = [i for i in range(30, 50)]
plt.plot(stockData)
plt.plot(elements)
#plt.fill_between(finalX, stockData[30:50], elements[30:50], alpha=0.4, color='red')
plt.show()