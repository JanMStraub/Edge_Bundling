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
Incomplete Cholesky Factorization
Code from: https://stackoverflow.com/questions/61508981/incomplete-cholesky-factorization-very-slow
"""
def incompleteCholeskyFactorization(A):
    n = A.shape[0]
    for k in range(n): 
        A[k,k] = np.sqrt(A[k,k])
        i_,_ = A[k + 1:,k].nonzero() 
        if len(i_) > 0:
            i_= i_ + (k + 1)
            A[i_,k] = A[i_,k]/A[k,k]
        for j in i_: 
            i2_,_ = A[j:n,j].nonzero()
            if len(i2_) > 0:
                i2_ = i2_ + j
                A[i2_,j]  = A[i2_,j] - A[i2_,k] * A[j,k]   

    return A


def ICCG(A):
    A = incompleteCholeskyFactorization(A)
    print(A)
    
    
    return A


"""_summary_
Calculates the distance between two nodes
"""
def calculateEdgeLength(node1, node2):
    return math.dist(node1._position, node2._position)


def initializeConductivity(edgeList, viscosity):
    for edge in edgeList:
        edge._conductivity = (np.pi * edge._radius ** 4) / (8 * viscosity)
    
    return


def calculateFlux(nodeList, edgeList):
    for edge in edgeList:
        pressureSum = 0
        for i in range(0, len(nodeList)):
            pressureSum += edge._start._pressureVector[i] - edge._end._pressureVector[i]
        edge._flux = (edge._conductivity / edge._length) * pressureSum
    
    return


def calculateConductivity(edgeList, sigma, rho):
    
    for edge in edgeList:
        edge._conductivity = edge._conductivity + (sigma * abs(edge._flux - rho * edge._cost * edge._conductivity))
    
    return


def calculatePressure(node, edgeList, initialFlow):
    
    if (node._sink == False):
        #node._pressureVector.clear() # Might have to change that
        
        for edge in node._nodeEdgeList:
            if edge._start._id != node._id:
                node._pressureVector.append((initialFlow * edge._length + edge._conductivity * edge._start._pressureVector[edge._id]) / edge._conductivity)
            if edge._end._id != node._id:
                node._pressureVector.append((initialFlow * edge._length + edge._conductivity * edge._end._pressureVector[edge._id]) / edge._conductivity)
            
    elif (node._sink == True):
        #node._pressureVector.clear()
        
        for edge in node._nodeEdgeList:
            node._pressureVector.append(0)
            
    else:
        #node._pressureVector.clear()
        
        for edge in node._nodeEdgeList:
            if edge._start._id != node._id:
                node._pressureVector.append((edge._conductivity * edge._start._pressureVector[edge._id]) / edge._conductivity)
            if edge._end._id != node._id:
                node._pressureVector.append((edge._conductivity * edge._end._pressureVector[edge._id]) / edge._conductivity)
    
    return