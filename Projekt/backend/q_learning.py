#!/usr/bin/env python3

from random import randint


class QLearning:
    qMatrix = []
    alpha = 0.5
    gamma = 0.5
    targetValue = 75
    minValue = 0
    maxValue = 100
    epsilon = 10
    phi = 0.2

    def __init__(self, initial_matrix):
        self.qMatrix = initial_matrix

    def get_q_matrix(self):
        return self.qMatrix

    def calculate_diff(self):
        return self.maxValue - self.minValue

    def calculate_reward(self, score):
        return self.calculate_diff() - abs(score - self.targetValue)

    def update_q_matrix(self, index, score):
        reward = self.calculate_reward(score)

        value = self.qMatrix[index]
        max_value = max(self.qMatrix)
        self.qMatrix[index] = value + self.alpha * (reward + self.gamma * max_value - value)

    def get_next(self):
        if randint(0, 100) < self.epsilon:
            return randint(0, len(self.qMatrix) - 1)

        copy = list(reversed(sorted(self.qMatrix)))

        # noinspection PyTypeChecker
        compare_value = copy[int(self.phi * len(copy))]

        matches = []
        for i in range(0, len(self.qMatrix)):
            if self.qMatrix[i] >= compare_value:
                matches.append(i)

        return matches[randint(0, len(matches) - 1)]


"""
x = QLearning(5)
x.update_q_matrix(0, 75)
x.update_q_matrix(1, 90)
x.update_q_matrix(3, 60)
print(x.get_q_matrix())
print("")
print(x.get_next())
"""
