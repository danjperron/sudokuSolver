import math

class  Statistic:
    def __init__(self):
        self.clear()

    def clear(self):
        self.count=0
        self.sum=0.0
        self.sumSquare=0.0

    def add(self, value):
        self.count += 1
        self.sum   += value
        self.sumSquare += (value * value)

    def mean(self):
        if self.count == 0:
            return 0.0
        return self.sum / self.count

    def sumOfVariance(self):
        if self.count < 2:
            return 0.0
        return self.sumSquare - ( self.mean() * self.sum)

    def stdev(self):
        if self.count < 2 :
            return 0.0
        stdevSqr = self.sumOfVariance() / (self.count - 1.0)
        if stdevSqr >= 0.0:
            return math.sqrt(stdevSqr)
        return 0.0








