# -*- coding: utf-8 -*-

"""
This algorithm is used to transfere different JSON formats
@author: Jan Straub
"""

# Imports
from json import load


def convert_graph(path):

    # read graph data from JSON
    with open(path, mode = "r", encoding = "utf-8") as file:
        data = load(file)

    nodes = data["nodes"]
    formatNodes = []
    
    for node in nodes:
        nodeCoords = []
        nodeCoords.append(node["id"])
        nodeCoords.append(node["x"])
        nodeCoords.append(node["y"])
        nodeCoords.append("0")
        formatNodes.append(nodeCoords)

    # Read relevant data
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
    paths = data["graph"]["edges"]

    # Convert node to tupel
    for i in range(len(nodes)):
        nodePosition = tuple(map(float, nodes[str(i)].strip("()").split(",")))
        print(f"{{\"x\": {nodePosition[0]}, \"y\": {nodePosition[1]}, \"id\": {i}}},")
    
    for path in paths:
        print(f"{{\"source\": \"{path[0]}\", \"target\": \"{path[1]}\"}},")


    # Read relevant data
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
    paths = data["graph"]["edges"]

    nodeList = []
    nodeListAppend = nodeList.append

    # Convert node to tupel
    for i in range(len(nodes)):
        nodePosition = tuple(map(float, nodes[str(i)].strip("()").split(",")))
        nodeListAppend(nodePosition[:2])

    return nodeList, paths

    
if __name__ == "__main__":

    # Setup parameter
    PATH = "/Users/jan/Documents/code/gitlab_BA/2023-jan-straub/"
    JSON_FILE_NAME = "10x10_10n_30e"
    JSON_FILE_PATH = PATH + "/data/" + JSON_FILE_NAME + ".json"

    convert_graph(JSON_FILE_PATH)