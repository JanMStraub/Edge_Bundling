import matplotlib.pyplot as plt
import json
import networkx as nx

dictionary = json.load(open('/Users/jan/Documents/Programmieren/bachelor_thesis/stuff/data/simple_graph.json', 'r'))

for value in dictionary["graph"]:
    print(value)

print(dictionary["graph"]["edges"])

G = nx.DiGraph()
G.add_edges_from(dictionary["graph"]["edges"])

