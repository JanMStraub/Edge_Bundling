# -*- coding: utf-8 -*-

# Imports
import json
import math


"""_summary_
Function for reading JSON file and converting string data to tupel
"""
def readGraphData(path):
    
    # read graph data from JSON
    file = open(path)
    data = json.load(file)
    file.close()
    
    # Read relevant data
    numberOfNodes = data["graph"]["nodesNumber"]
    numberOfEdges = data["graph"]["edgesNumber"]
    edges = data["graph"]["edges"]
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
    
    nodeList = []
    
    # Convert node to tupel
    for i in range(len(nodes)):
        nodeList.append(tuple(map(int, nodes[str(i)].strip("()").split(','))))
    
    return edges, nodeList, numberOfEdges, numberOfNodes


"""_summary_
Calculates the distance between two nodes
"""
def calculateEdgeLength(node1, node2):
    return math.dist(node1._position, node2._position)


def findNodeById(id, nodeList):
    for node in nodeList:
        if (node._id == id):
            return node