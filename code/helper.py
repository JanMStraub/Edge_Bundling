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
Function calculats the horizontal edge cost from equation (12)
"""
def horizontalIntegrand(x2, x1, y1, y2, gamma):
    return ((math.sqrt((x2 - x1)**2 + (y2 - y1)**2))) * gamma


"""_summary_
Function calculats the vertical edge cost from equation (12)
"""
def verticalIntegrand(y2, x1, y1, x2, gamma):
    return ((math.sqrt((x2 - x1)**2 + (y2 - y1)**2))) * gamma


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
    
    
def findEdgeBetweenNodes(edgeList, node1, node2):
    
    for edge in edgeList:
        if(edge._start == node1 and edge._end == node2) or (edge._start == node2 and edge._end == node1):
            return edge
        else:
            raise ValueError("No edge between node{} and node{}".format(node1._id, node2._id))