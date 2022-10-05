# -*- coding: utf-8 -*-

# Imports
import random

import numpy as np

from scipy.integrate import quad
from tqdm import tqdm

from helper import findOtherEdgeEnd, horizontalIntegrand, verticalIntegrand

   
"""_summary_
Edge cost calculation from the paper
"""
def initializeEdgeCost(edge, terminalNodeList, gamma):
    
    # vertical edge
    if (edge._start._position[0] == edge._end._position[0]):
        a = edge._start._position[1]
        b = edge._start._position[1] + edge._length
        x2, y2, z2 = edge._start._position
        
        for terminal in terminalNodeList:
            x1, y1, z1 = terminal._position
            I = quad(verticalIntegrand, a, b, args = (x1, y1, x2, gamma))[0]
            edge._cost += abs(I)  

    # horizontal edge
    elif (edge._start._position[1] == edge._end._position[1]):
        a = edge._start._position[0]
        b = edge._start._position[0] + edge._length
        x2, y2, z2 = edge._start._position
        
        for terminal in terminalNodeList:
            x1, y1, z1 = terminal._position
            I = quad(horizontalIntegrand, a, b, args = (x1, y1, y2, gamma))[0]
            edge._cost += abs(I)
    
    return


"""_summary_
Initializes the conductivity (D_0) of all edges according to equation (1)
"""
def initializeConductivity(edge, viscosity):
    edge._conductivity[0] = edge._conductivity[1] = (np.pi * edge._radius ** 4) / (8 * viscosity)
    
    return


"""_summary_
Initializes the pressure vector (p^0) in all nodes according to equation (4). 
"""
def initializePressure(A, b, nodeList, terminalNodeList, initialFlow):
    
    for node in nodeList:
        
        if (node._sink == False and node._terminal == True):
            pressureVector = [0] * len(nodeList)
            
            for entry in nodeList:
                for neighbour in node._neighbours:
                    if (entry._id == node._id):
                        pressureVector[entry._id] = node._connections * node._initialPressure
                    elif (entry._id == neighbour._id):
                        pressureVector[entry._id] = -1 * node._initialPressure
            
            b.append((initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity[0])
            A.append(pressureVector)            
        
        elif (node._sink == True and node._terminal == True):
            pressureVector = [0] * len(nodeList)
            
            for entry in nodeList:
                for neighbour in node._neighbours:
                    if (entry._id == neighbour._id):
                        pressureVector[entry._id] = node._initialPressure
            
            b.append(((len(terminalNodeList) - 1) * initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity[0])
            A.append(pressureVector)       
        
        elif (node._sink == False and node._terminal == False):
            pressureVector = [0] * len(nodeList)
            
            for entry in nodeList:
                for neighbour in node._neighbours:
                    if (entry._id == node._id):
                        pressureVector[entry._id] = node._connections * node._initialPressure
                    elif (entry._id == neighbour._id):
                        pressureVector[entry._id] = -1 * node._initialPressure
            
            b.append(0)
            A.append(pressureVector)

    return


def calculateCompositeCost(edge):
    
    
    return 


def calculateFlux(edge):
    
    
    
    return


"""_summary_
Calculates the conductivity (D^t+1) throught each edge using equation (6)
"""
def calculateConductivity(currentNode, edge, terminalNodeListLength, edgeList, sigma, rho, tau, viscosity):
        
    pressureSum = 0
    for i in range(terminalNodeListLength):
        pressureSum += edge._start._pressureVector[i] - edge._end._pressureVector[i]
    
    kappa = 1 + sigma * ((abs(pressureSum)) / edge._length) - rho * edge._cost
    
    edge._conductivity[1] = kappa * edge._conductivity[0]
    edge._radius = calculateRadius(edge, viscosity)

    # edge cutting
    if edge in edgeList and edge._conductivity[1] < tau:
        otherEnd = findOtherEdgeEnd(currentNode, edge)
        
        currentNode._nodeEdgeList.remove(edge)
        otherEnd._nodeEdgeList.remove(edge)
        
        currentNode._connections -= 1
        otherEnd._connections -= 1
        
        currentNode._neighbours.remove(otherEnd)
        otherEnd._neighbours.remove(currentNode)
        
        currentNode._neighbourIDs.remove(otherEnd._id)
        otherEnd._neighbourIDs.remove(currentNode._id)
        
        edgeList.remove(edge)
    
    return


"""_summary_
Approximates the pressure change (p^t+1) for each node using equation (9)
"""
def calculatePressure(currentNode, terminalNodeListLength, initialFlow):

    for i in range(terminalNodeListLength):
        if (currentNode._terminal == True and currentNode._terminalId != i):
            conductivitySum = 0
            conductivityPressureSum = 0
            
            for edge in currentNode._nodeEdgeList:
                conductivitySum += edge._conductivity[1]
                conductivityPressureSum += edge._conductivity[1] * (currentNode._pressureVector[i] + findOtherEdgeEnd(currentNode, edge)._pressureVector[i])
            
            currentNode._pressureVector[i + terminalNodeListLength] = ((initialFlow * 1 + conductivityPressureSum) / (conductivitySum * 2))
            
        elif (currentNode._terminal == True and currentNode._terminalId == i):
            currentNode._pressureVector[i + terminalNodeListLength] = 0
            
        elif (currentNode._terminal == False):
            conductivitySum = 0
            conductivityPressureSum = 0
            
            for edge in currentNode._nodeEdgeList:
                conductivitySum += edge._conductivity[1]
                conductivityPressureSum += edge._conductivity[1] * (currentNode._pressureVector[i] + findOtherEdgeEnd(currentNode, edge)._pressureVector[i])
            
            currentNode._pressureVector[i + terminalNodeListLength] = (conductivityPressureSum / (conductivitySum * 2))
            
        else:
            raise ValueError("Node not supported")

    return


"""_summary_
Calculates radius of each edge, derived from equation (1)
"""
def calculateRadius(edge, viscosity):
    return ((edge._conductivity[1] * 8 * viscosity) / np.pi) ** (1 / 4)


def updateCalculations(edgeList, nodeList, terminalNodeListLength):
    
    for edge in edgeList:
        edge._conductivity[0] = edge._conductivity[1]    
    
    for node in nodeList:
        for i in range(terminalNodeListLength):
            node._pressureVector[i] = node._pressureVector[i + terminalNodeListLength]
    
    return


def chooseSinkAndSource(nodeList, terminalNodeList):
    l = []
    T = len(terminalNodeList)
    edgeCostSum = 0
    
    for terminal in terminalNodeList:
        totalEdgeCost = 0
        for edge in terminal._nodeEdgeList:
            totalEdgeCost += edge._cost

        terminal._totalEdgeCost = totalEdgeCost
        edgeCostSum += totalEdgeCost
        l.append(terminal)
        
    l.sort(key = lambda terminal: terminal._totalEdgeCost)

    sink = l[T - i + 1]._totalEdgeCost / edgeCostSum
    
    return


def calculatePressure(A, b, nodeList, terminalNodeList, initialFlow):
    
    for node in nodeList:
        
        if (node._sink == False and node._terminal == True):
            pressureVector = [0] * len(nodeList)

            for entry in nodeList:
                for neighbour in node._neighbours:
                    if (entry._id == node._id):
                        pressureVector[entry._id] = node._connections * node._initialPressure
                    elif (entry._id == neighbour._id):
                        pressureVector[entry._id] = -1 * node._initialPressure
            
            b.append((initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity[0])
            A.append(pressureVector)            
        
        elif (node._sink == True and node._terminal == True):
            pressureVector = [0] * len(nodeList)
            
            for entry in nodeList:
                for neighbour in node._neighbours:
                    if (entry._id == neighbour._id):
                        pressureVector[entry._id] = node._initialPressure
            
            b.append(((len(terminalNodeList) - 1) * initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity[0])
            A.append(pressureVector)       
        
        elif (node._sink == False and node._terminal == False):
            pressureVector = [0] * len(nodeList)
            
            for entry in nodeList:
                for neighbour in node._neighbours:
                    if (entry._id == node._id):
                        pressureVector[entry._id] = node._connections * node._initialPressure
                    elif (entry._id == neighbour._id):
                        pressureVector[entry._id] = -1 * node._initialPressure
            
            b.append(0)
            A.append(pressureVector)
    
    return
    

"""_summary_
Function is used to calculate each time step in the simulation
"""
def physarumAlgorithm(nodeList, terminalNodeList, edgeList, viscosity, initialFlow, sigma, rho, tau):
    maxNodeWeight = 0
    
    for node in nodeList:
        if (node._weight > maxNodeWeight):
            maxNodeWeight = node._weight 
            
    for edge in edgeList:
        initializeConductivity(edge, viscosity)   
    
    K = 1
    
    for k in tqdm(range(K), desc = "Inner iteration progress"):
        A = []
        b = []
        
        chooseSinkAndSource(nodeList, terminalNodeList)
        calculatePressure(A, b, nodeList, terminalNodeList, initialFlow)
    
    random.shuffle(nodeList)

    for node in nodeList:
        for edge in node._nodeEdgeList:
            if (edge._conductivity[0] == edge._conductivity[1]):
                calculateConductivity(node, edge, len(terminalNodeList), edgeList, sigma, rho, tau, viscosity)
        
        if node._connections != 0:
            calculatePressure(node, len(terminalNodeList), initialFlow)
        else:
            nodeList.remove(node)
            
    updateCalculations(edgeList, nodeList, len(terminalNodeList))
    
    return