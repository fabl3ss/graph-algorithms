from pyvis.network import Network
import numpy as np
from math import isinf
from sweater.build_page import build_page


class MyNetwork:
    def __init__(self) -> None:
        self.network = Network(height='1000px', width='50%', bgcolor='#222222', font_color='white')
        self.network.barnes_hut(spring_length=300)
        self.network.set_edge_smooth('dynamic')

        #self.network.hrepulsion()
        self.network.set_options(open('options/network_options.txt', 'r').read())
        #self.network.show_buttons()

    def map_data(self, matrix):
        for i in range(np.shape(matrix)[0]):
            self.network.add_node(i)

        for i in range(np.shape(matrix)[0]):
            for j in range(np.shape(matrix)[1]):
                if not isinf(matrix[i][j]):
                    self.network.add_edge(i, j, title=matrix[i][j], width=matrix[i][j])

        edges = self.network.get_edges()
        for i in range(np.shape(matrix)[0]):
            value = 10000
            for edge in edges:
                if edge['from'] == i:
                    value += 1
            self.network.get_node(i)['value'] = value

    def draw_graph(self):
        self.network.write_html("sweater/templates/network.html")
        build_page()

    def highlight_path(self, source, target, color="green"):
        edges = self.network.get_edges()
        for edge in edges:
            if edge['from'] == source and edge['to'] == target:
                edge['color'] = color
                edge['value'] = 10

    def restore_path(self):
        edges = self.network.get_edges()
        for edge in edges:
            edge['color'] = {"highlight": "rgba(132,48,51,1)",
                             "hover": "rgba(128,25,132,1)"}
            edge['value'] = 0
