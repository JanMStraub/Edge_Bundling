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
    
    
def findEdgeBetweenNodes(edgeList, node1, node2):
    for edge in edgeList:
        print(edge._start._id)
        print(edge._end._id)
        print(node1._id)
        print(node2._id)
        
        print()
        
        if(edge._start == node1 and edge._end == node2) or (edge._start == node2 and edge._end == node1):
            return edge