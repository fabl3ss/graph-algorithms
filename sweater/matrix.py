from math import inf
from random import randint


class Matrix:
    def __init__(self, matrix_size) -> None:
        self.adjacency = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]
        self.weights = [[inf for _ in range(matrix_size)] for _ in range(matrix_size)]
        self.size = matrix_size
        self.fill_random_matrix()

    def fill_random_matrix(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.adjacency[j][i] == 0 and self.adjacency[i][j] == 0 and j != i:
                    self.adjacency[i][j] = randint(0, 1)

        for i in range(self.size):
            for j in range(self.size):
                if self.adjacency[i][j] == 1:
                    self.weights[i][j] = randint(0, 10)

