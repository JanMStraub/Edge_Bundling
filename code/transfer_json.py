# -*- coding: utf-8 -*-

"""
This algorithm is used to transfer between json formats
@author: Jan Straub
"""

# Imports
from json import load
import random

def convert_graph(path):

    """_summary_
        Function for reading JSON file and converting string data to tupel
    Returns:
        nodeList (list): A list of the original nodes positions
        paths (list) : A list of the original paths
    """

    # read graph data from JSON
    with open(path, mode = "r", encoding = "utf-8") as file:
        data = load(file)
    """
    nodes = data["nodes"]
    formatNodes = []
    
    for node in nodes:
        nodeCoords = []
        nodeCoords.append(node["id"])
        nodeCoords.append(node["x"])
        nodeCoords.append(node["y"])
        nodeCoords.append("0")
        formatNodes.append(nodeCoords)
    """
    # Read relevant data
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
    paths = data["graph"]["edges"]

    # Convert node to tupel
    for i in range(len(nodes)):
        nodePosition = tuple(map(float, nodes[str(i)].strip("()").split(",")))
        print(f"{{\"x\": {nodePosition[0]}, \"y\": {nodePosition[1]}, \"id\": {i}}},")
    
    for path in paths:
        print(f"{{\"source\": \"{path[0]}\", \"target\": \"{path[1]}\"}},")


    """
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
    """
    
def random_graph():
    numberOfNodes = 10
    numberOfEdges = 30
    size = 10
    
    nodeList = random_nodes(numberOfNodes, size)
    random_edges(numberOfNodes, numberOfEdges, nodeList)

def random_nodes(numberOfNodes, size):
    nodeList = []
    id = 0
    while id < numberOfNodes:
        x = random.randrange(0, size)
        y = random.randrange(0, size)
        if [x, y] not in nodeList and [y, x] not in nodeList:
            nodeList.append([x, y])
            print(f"\"{id}\": \"({x},{y},0)\",")
            id += 1

    return nodeList

def random_edges(numberOfNodes, numberOfEdges, nodeList):
    edgeList, edgeStartList, edgeEndList = [], [], []
    iterator = 0
    
    while iterator < numberOfEdges:
        start = random.randrange(0, numberOfNodes)
        end = random.randrange(0, numberOfNodes)
        if start != end:
            if [start, end] not in edgeList and [end, start] not in edgeList:
                edgeList.append([start, end])
                edgeStartList.append(start)
                edgeEndList.append(end)
                print(f"[{start}, {end}],")
                iterator += 1

    for i in range(0, len(nodeList)):
        if i in edgeStartList or i in edgeEndList:
            continue
        else:
            raise ValueError("Not all nodes have edges")

    
if __name__ == "__main__":

    # Setup parameter
    PATH = "/Users/jan/Documents/code/gitlab_BA/2023-jan-straub/"
    JSON_FILE_NAME = "10x10_10n_30e"
    JSON_FILE_PATH = PATH + "/data/" + JSON_FILE_NAME + ".json"

    convert_graph(JSON_FILE_PATH)
    #random_graph()