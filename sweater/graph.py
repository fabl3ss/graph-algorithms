from sweater.matrix import Matrix
from sweater.net import MyNetwork
from sweater.algorithms import Bellman, Dijkstra, Floyd, Johnson


class Graph:
    def __init__(self, size):
        self.matrix = Matrix(size)
        self.network = MyNetwork()
        self.network.map_data(matrix=self.matrix.weights)
        self.network.draw_graph()
        self.size = size

        # Shortest path algorithms
        self.bellman = Bellman(self.matrix)
        self.dijkstra = Dijkstra(self.matrix)
        self.floyd = Floyd(self.matrix)
        self.johnson = Johnson(self.matrix)

    def draw_path(self, parent, j, source):
        if parent[j] == -1:
            self.network.highlight_path(j, source)
            return
        self.network.highlight_path(parent[j], j)
        self.draw_path(parent, parent[j], source)

