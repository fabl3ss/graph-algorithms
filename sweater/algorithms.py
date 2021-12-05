from math import inf, isinf
from copy import deepcopy
import json


class Bellman:

    def __init__(self, matrix):
        self.matrix = matrix
        self.path = ""

    def _get_path(self, parent, j, source):
        if parent[j] == -1:
            self.path += (str(j) + ' ')
            return
        self._get_path(parent, parent[j], source)
        self.path += (str(j) + ' ')

    def _print_path(self, dist, parent, source, target):
        # Delete previous path
        self.path = ""

        print(self._get_path(parent, target, source))
        response = {
            "response": [
                {
                    'algorithm': 'BELLMAN',
                    'source': source,
                    'target': target,
                    'dist': dist[target],
                    'path': self.path
                }
            ]
        }
        with open('options/response.json', 'w') as outfile:
            json.dump(response, outfile)

    def bellman_algorithm(self, source):
        dist = [inf] * self.matrix.size
        parent = [-1] * self.matrix.size

        # переделать под пример с https://favtutor.com/blogs/bellman-ford-python
        dist[source] = 0

        for k in range(1, self.matrix.size):
            for i in range(self.matrix.size):
                for j in range(self.matrix.size):
                    if dist[j] + self.matrix.weights[j][i] < dist[i]:
                        dist[i] = dist[j] + self.matrix.weights[j][i]
                        parent[i] = j
        return dist[0:len(self.matrix.weights)], parent

    def run(self, source, target):
        dist, parent = self.bellman_algorithm(source)
        self._print_path(dist, parent, source, target)


class Floyd:

    def __init__(self, matrix):
        self.matrix = matrix
        self.path = ""
        self._next = [[-1 for _ in range(matrix.size)] for _ in range(matrix.size)]

        for i in range(self.matrix.size):
            for j in range(self.matrix.size):
                if isinf(self.matrix.weights[i][j]):
                    self._next[i][j] = -1
                else:
                    self._next[i][j] = j

    def _get_path(self, source, target):
        if self._next[source][target] == -1:
            return

        while source != target:
            source = self._next[source][target]
            self.path += (str(source) + ' ')

    def _print_path(self, dist, source, target):
        # Delete previous path
        self.path = str(source) + ' '

        self._get_path(source, target)
        response = {
            "response": [
                {
                    'algorithm': 'FLOYD',
                    'source': source,
                    'target': target,
                    'dist': dist[source][target],
                    'path': self.path
                }
            ]
        }
        with open('options/response.json', 'w') as outfile:
            json.dump(response, outfile)

    def floyd_algorithm(self):
        dist = deepcopy(self.matrix.weights)
        for k in range(self.matrix.size):
            for i in range(self.matrix.size):
                for j in range(self.matrix.size):

                    # We cannot travel through
                    # edge that doesn't exist
                    if isinf(dist[i][k]) or isinf(dist[k][j]):
                        continue
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        self._next[i][j] = self._next[i][k]

        return dist

    def run(self, source, target):
        self._print_path(self.floyd_algorithm(), source, target)


class Dijkstra:

    def __init__(self, matrix):
        self.matrix = matrix
        self.path = ""

    def _get_path(self, parent, j, source):
        if parent[j] == -1:
            self.path += (str(j) + ' ')
            return
        self._get_path(parent, parent[j], source)
        self.path += (str(j) + ' ')

    def _print_path(self, dist, parent, source, target):
        # Delete previous path
        self.path = ""

        print(self._get_path(parent, target, source))
        response = {
            "response": [
                {
                    'algorithm': 'DIJKSTRA',
                    'source': source,
                    'target': target,
                    'dist': dist[target],
                    'path': self.path
                }
            ]
        }
        with open('options/response.json', 'w') as outfile:
            json.dump(response, outfile)

    @staticmethod
    # FIXME: Sometimes min_index equal -1
    def __min_distance(dist, queue):
        # Initialize min value and min_index as -1
        minimum = float("Inf")
        min_index = -1

        # from the dist array,pick one which
        # has min value and is till in queue
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def dijkstra_algorithm(self, graph, source):
        # The output array. dist[i] will hold
        # the shortest distance from src to i
        # Initialize all distances as INFINITE
        dist = [float("Inf")] * self.matrix.size

        # Parent array to store
        # shortest path tree
        parent = [-1] * self.matrix.size

        # Distance of source vertex
        # from itself is always 0
        dist[source] = 0

        # Add all vertices in queue
        queue = []
        for i in range(self.matrix.size):
            queue.append(i)

        # Find shortest path for all vertices
        while queue:

            # Pick the minimum dist vertex
            # from the set of vertices
            # still in queue
            u = self.__min_distance(dist, queue)

            # remove min element
            queue.remove(u)

            # Update dist value and parent
            # index of the adjacent vertices of
            # the picked vertex. Consider only
            # those vertices which are still in
            # queue
            for i in range(self.matrix.size):
                if not isinf(graph[u][i]) and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u

        return dist, parent

    def run(self, source, target):
        dist, parent = self.dijkstra_algorithm(self.matrix.weights, source)
        self._print_path(dist, parent, source, target)


class Johnson(Dijkstra, Bellman):

    def __init__(self, matrix):
        super().__init__(matrix)

    def __create_modified(self, source):
        edges = []
        for i in range(self.matrix.size):
            for j in range(self.matrix.size):
                if not isinf(self.matrix.weights[i][j]):
                    edges.append([i, j, self.matrix.weights[i][j]])

        modify_weights, _ = self.bellman_algorithm(source)

        print(modify_weights)

        modified_graph = [[0 for _ in range(self.matrix.size)] for _ in
                          range(self.matrix.size)]

        for i in range(self.matrix.size):
            for j in range(self.matrix.size):
                if self.matrix.adjacency[i][j] != 0:
                    modified_graph[i][j] = (self.matrix.weights[i][j] + modify_weights[i] - modify_weights[j])

        import numpy as np
        print(np.matrix(modified_graph))
        return modified_graph

    def run(self, source, target):
        dist, parent = self.dijkstra_algorithm(self.__create_modified(source), source)
        self._print_path(dist, parent, source, target)
