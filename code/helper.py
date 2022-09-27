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
    return (1 / (math.sqrt((x2 - x1)**2 + (y2 - y1)**2))) * gamma


"""_summary_
Function calculats the vertical edge cost from equation (12)
"""
def verticalIntegrand(y2, x1, y1, x2, gamma):
    return (1 / (math.sqrt((x2 - x1)**2 + (y2 - y1)**2))) * gamma


"""_summary_
Calculates the distance between two nodes
"""
def calculateDistanceBetweenPositions(position1, position2):
    return math.dist(position1, position2)


"""_summary_
Function finds node by id
"""
def findNodeById(id, nodeList):
    for node in nodeList:
        if (node._id == id):
            return node


"""_summary_
Function used to specific node object in node grid
"""
def findNodeByPosition(nodeList, x, y, z):
    for node in nodeList:
        if node._position[0] == x and node._position[1] == y and node._position[2] == z: 
            return node
      
    
"""_summary_
Function used to find the edge that connects the two input nodes
"""
def findConnection(startNode, endNode):
    for edge in startNode._nodeEdgeList:
        if (startNode._id == edge._start._id or startNode._id == edge._end._id) and (endNode._id == edge._start._id or endNode._id == edge._end._id):
            return edge
        else:
            raise ValueError("No edge connecting node {} and {} was found".format(startNode._id, endNode._id))

        
"""_summary_
Function used to find the other end of an edge
"""
def findOtherEdgeEnd(node, edge):
    if (edge._start._id == node._id):
        return edge._end
    elif (edge._end._id == node._id):
        return edge._start