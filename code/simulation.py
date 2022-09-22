# -*- coding: utf-8 -*-

# Imports
import random
import math

import numpy as np

from scipy.integrate import quad

from helper import findOtherEdgeEnd, horizontalIntegrand, verticalIntegrand

   
"""_summary_
Edge cost calculation from the paper
"""
def initializeEdgeCost(edge, sensorNodeList):
    
    # vertical edge
    if (edge._start._position[0] == edge._end._position[0]):
        a = 0
        b = 1
        x2, y2, z2 = edge._start._position
        
        for sensor in sensorNodeList:
            x1, y1, z1 = sensor
            I = quad(verticalIntegrand, a, b, args = (x1, y1, x2))[0]
            edge._cost += abs(I)  

    # horizontal edge
    elif (edge._start._position[1] == edge._end._position[1]):
        a = 0
        b = 1
        x2, y2, z2 = edge._start._position
        
        for sensor in sensorNodeList:
            x1, y1, z1 = sensor
            I = quad(horizontalIntegrand, a, b, args = (x1, y1, y2))[0]
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


"""_summary_
Calculates the conductivity (D^t+1) throught each edge using equation (6)
"""
def calculateConductivity(currentNode, terminalNodeListLength, edgeList, sigma, rho, tau, viscosity):
        
    for edge in currentNode._nodeEdgeList:

        pressureSum = 0
        for i in range(terminalNodeListLength):
            pressureSum += edge._start._currentPressureVector[i] - edge._end._currentPressureVector[i]
        
        kappa = 1 + sigma * ((abs(pressureSum)) / edge._length) - rho * edge._cost

        edge._conductivity[1] = edge._conductivity[0] * kappa
        edge._radius = calculateRadius(edge, viscosity)

        # edge cutting
        if edge in edgeList and edge._conductivity[1] < tau:
            otherEnd = findOtherEdgeEnd(currentNode, edge)
            currentNode._nodeEdgeList.remove(edge)
            currentNode._connections -= 1
            otherEnd._connections -= 1
            currentNode._neighbours.remove(otherEnd)
            currentNode._neighbourIDs.remove(otherEnd._id)
            edgeList.remove(edge)
            # print("Edge ID: {} removed - tau: {}".format(edge._id, tau))
                
        
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
                conductivityPressureSum += edge._conductivity[1] * (currentNode._currentPressureVector[i] + findOtherEdgeEnd(currentNode, edge)._currentPressureVector[i])
            
            currentNode._nextPressureVector[i] = (initialFlow * 1 + conductivityPressureSum) / (conductivitySum * 2)
            
        elif (currentNode._terminal == True and currentNode._terminalId == i):
            currentNode._nextPressureVector[i] = 0.0
            
        elif (currentNode._terminal == False):
            conductivitySum = 0
            conductivityPressureSum = 0
            for edge in currentNode._nodeEdgeList:
                conductivitySum += edge._conductivity[1]
                conductivityPressureSum += edge._conductivity[1] * (currentNode._currentPressureVector[i] + findOtherEdgeEnd(currentNode, edge)._currentPressureVector[i])
            
            currentNode._nextPressureVector[i] = conductivityPressureSum / (conductivitySum * 2)
    return


"""_summary_
Calculates radius of each edge, derived from equation (1)
"""
def calculateRadius(edge, viscosity):
    return ((edge._conductivity[1] * 8 * viscosity) / np.pi) ** (1 / 4)


"""_summary_
Function is used to initialize the Physarium simulation by setting the initial conductivity and pressure
"""
def initializePhysarium(edgeList, nodeList, terminalNodeList, sensorNodeList, viscosity = 1.0, initialFlow = 10.0):
    
    for edge in edgeList:
        initializeConductivity(edge, viscosity)
        initializeEdgeCost(edge, sensorNodeList)
    
    for node in terminalNodeList:
        A = list()            
        b = list()
        
        node._sink = True
        initializePressure(A, b, nodeList, terminalNodeList, initialFlow)
        
        node._sink = False

        A = np.array(A)
        b = np.array(b)
        x = np.linalg.solve(A, b)

        for i in range(len(nodeList)):
            nodeList[i]._nextPressureVector.append(x[i])
            nodeList[i]._currentPressureVector.append(x[i])

    return
    

"""_summary_
Function is used to calculate each time step in the simulation
"""
def physarumAlgorithm(nodeList, terminalNodeList, edgeList, viscosity = 1.0, initialFlow = 0.5, sigma = 0.00000375, rho = 0.0002, tau = 0.0004):
    random.shuffle(nodeList)

    for node in nodeList:
        for neighbour in node._neighbours:
            calculateConductivity(node, len(terminalNodeList), edgeList, sigma, rho, tau, viscosity)
        
        if node._connections != 0:
            calculatePressure(node, len(terminalNodeList), initialFlow)
    
    return


def updateCalculations(edgeList, nodeList):
    
    for edge in edgeList:
        edge._conductivity[0] = edge._conductivity[1]    
    
    for node in nodeList:
        node._currentPressureVector = node._nextPressureVector
    
    return