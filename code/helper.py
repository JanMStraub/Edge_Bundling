# -*- coding: utf-8 -*-

# Imports
import json
import math

import numpy as np

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
    for i in range(0, len(nodes)):
        nodeList.append(tuple(map(int, nodes[str(i)].strip("()").split(','))))
    
    return edges, nodeList, numberOfEdges, numberOfNodes


"""_summary_
Calculate points between edges
Code from: https://stackoverflow.com/questions/25837544/get-all-points-of-a-straight-line-in-python
"""
def calculateEdges(node1, node2):
    
    points = []
    ystep = None
    
    x1, y1, z1 = node1._position
    x2, y2, z2 = node2._position
    issteep = abs(y2 - y1) > abs(x2 - x1)
    
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        
    deltax = x2 - x1
    deltay = abs(y2 - y1)
    error = int(deltax / 2)
    y = y1
    
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
        
    return points


"""_summary_
Calculates the distance between two nodes
"""
def calculateEdgeLength(node1, node2):
    return math.dist(node1._position, node2._position)


def initializeConductivity(edgeList, viscosity):
    for edge in edgeList:
        edge._conductivity = (np.pi * edge._radius ** 4) / (8 * viscosity)
    
    return


def initializePressure(nodeList, initialFlow):
    A = list()
    b = list()
    
    for node in nodeList:
        
        if (node._sink == False):
            pressureList = list()
            
            for i in range(0, node._connections + 1):
                if (i == node._id):
                    pressureList.extend([node._connections * node._pressure])
                else:
                    pressureList.extend([-1 * node._pressure])
                
            b.append((initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity)
            A.append(pressureList)
            
        elif (node._sink == True):
            pressureList = list()
            
            for i in range(0, node._connections + 1):
                if (i == node._id):
                    pressureList.extend([node._connections * node._pressure])
                else:
                    pressureList.extend([0])
                
            b.append(((len(nodeList) - 1) * initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity)
            A.append(pressureList)
        else:
            pressureList = list()
            
            for i in range(0, node._connections + 1):
                if (i == node._id):
                    pressureList.extend([node._connections * node._pressure])
                else:
                    pressureList.extend([-1 * node._pressure])
            
            b.append(0)
            A.append(pressureList)
            
    A = np.array(A)
    b = np.array(b)
    x = np.linalg.solve(A, b)
    
    for i in range(len(nodeList)):
        nodeList[i]._pressure = x[i]
        nodeList[i]._pressureVector.append(x[i])
    
    return