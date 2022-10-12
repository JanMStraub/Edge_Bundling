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
    edges = data["graph"]["edges"]
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
    
    nodeList = []
    
    # Convert node to tupel
    for i in range(len(nodes)):
        nodeList.append(tuple(map(float, nodes[str(i)].strip("()").split(','))))
    
    return edges, nodeList


"""_summary_
Calculates the distance between two nodes
"""
def calculateDistanceBetweenPositions(position1, position2):
    return math.dist(position1, position2)


"""_summary_
Function used to specific node object in node grid
"""
def findNodeByPosition(nodeList, x, y, z):
    for node in nodeList:
        if node._position[0] == x and node._position[1] == y and node._position[2] == z: 
            return node
        

"""_summary_
Function used to find the other end of an edge
"""
def findOtherEdgeEnd(node, edge):
    if (edge._start._id == node._id):
        return edge._end
    elif (edge._end._id == node._id):
        return edge._start