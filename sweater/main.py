import json

from sweater.graph import Graph

graph_settings = json.load(open('options/properties.json', ))['graph']
graph = Graph(graph_settings['size'])
