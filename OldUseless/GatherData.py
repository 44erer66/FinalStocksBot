import pandas as pd


class Properties():
    def __init__(self, symbol):

        self.data = pd.read_csv("MinuteData/"+symbol+".csv")




    def opens(self):
        x = []
        for i in self.dayGroupedData():
            x.append(i[0])
        return x

    def current(self):
        x = []
        o = list(self.data['time'])
        for j in range(len(list(self.data['open'])[::-1])):
            i = o[j]
            if 6 <= int(i.split(' ')[1].split(":")[0]) <= 13:
                x.append(list(self.data['open'])[::-1][j])

        return x
    #20:00:00
    def times(self):
        x = []
        o = list(self.data['time'])
        for i in o:
            if 6 <= int(i.split(' ')[1].split(":")[0]) <= 13:
                x.append(i.split(' ')[0])

        return x[::-1]



    def preciseTimes(self):
        xo = []
        o = list(self.data['time'])
        for i in o:

            time = i.split(' ')[1]
            splitTime = time.split(':')
            h, m = int(splitTime[0]), int(splitTime[1])
            if 6 <= h <= 13:
                xo.append(h*100 + m*1)
        xo.reverse()
        referenceList = self.times()
        curr = referenceList[0]
        x = []
        o = []
        current = self.current()

        for time in range(len(current)):

            if referenceList[time] == curr:
                o.append(xo[time])
            else:
                a = list(o)

                x.append(a)

                curr = referenceList[time]
                o.clear()
                o.append(xo[time])
        x.append(o)

        return x
    def dayGroupedData(self):
        referenceList = self.times()
        current = self.current()


        curr = referenceList[0]
        x = []
        o = []


        for time in range(len(current)):

            if referenceList[time] == curr:
                o.append(current[time])
            else:
                a = list(o)

                x.append(a)

                curr = referenceList[time]
                o.clear()
                o.append(current[time])
        x.append(o)
        return x



