import math;
from random import randint;

class QLearning:
    qMatrix = [];
    alpha = 0.5;
    gamma = 0.5;
    targetValue = 75;
    minValue = 0;
    maxValue = 100;
    
    epsilon = 10;
    phi = 0.2;

    def __init__(self, states):
        self.qMatrix = [0.0]*states;

    def getQMatrix(self):
        return self.qMatrix;

    def calculateDiff(self):
        return self.maxValue - self.minValue;

    def calculateReward(self, score):
        return self.calculateDiff() - abs(score - self.targetValue);

    def updateQMatrix(self, index, score):
        reward = self.calculateReward(score);
        
        value = self.qMatrix[index];
        maxValue = max(self.qMatrix);
        self.qMatrix[index] = value + self.alpha * (reward + self.gamma * maxValue - value)

    def getNext(self):
        random = randint(0,100);
        if(random < self.epsilon):
            return randint(0, len(self.qMatrix) - 1);
        copy = list(self.qMatrix);
        copy.sort();
        copy.reverse();
        compareValue = copy[int(self.phi * len(copy))];
        matches = [];
        for i in range(0, len(self.qMatrix)):
            if(self.qMatrix[i] >= compareValue):
                matches.append(i);

        return matches[randint(0, len(matches) - 1)];


x = QLearning(5);
x.updateQMatrix(0, 75);
x.updateQMatrix(1, 90);
x.updateQMatrix(3, 60);
print(x.getQMatrix());
print("");
print(x.getNext());
