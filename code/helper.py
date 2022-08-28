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
        nodeList.append(tuple(map(float, nodes[str(i)].strip("()").split(','))))
    
    return edges, nodeList, numberOfEdges, numberOfNodes


"""_summary_
Calculates the distance between two nodes
"""
def calculateEdgeLength(node1, node2):
    return math.dist(node1._position, node2._position)


"""_summary_
Function used to specific node object in node grid
"""
def findNodeByPosition(nodeList, x, y, z):
    for node in nodeList:
        if node._position[0] == x and node._position[1] == y and node._position[2] == z: 
            return node
        

"""_summary_
Use A* to find shortest path in grid graph
"""
def findShortestPath(nodeList, startNode, endNode):
    gCost, hCost, fCost = 0, 0, 0
    
    
    
    return