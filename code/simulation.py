# -*- coding: utf-8 -*-

# Imports
import numpy as np


"""_summary_
Initializes the conductivity (D_0) of all edges according to equation (1)
"""
def initializeConductivity(edgeList, viscosity):
    for edge in edgeList:
        edge._conductivity = (np.pi * edge._radius ** 4) / (8 * viscosity)
    
    return


"""_summary_
Initializes the pressure vector (p^0) in all nodes according to equation (4). 
"""
def initializePressure(nodeList, initialFlow):
    
    for sinkNode in nodeList:
        if sinkNode._terminal == True:
            sinkNode._sink = True
            
            A = list()
            b = list()
            
            for node in nodeList:

                if (node._sink == False and node._terminal == True):
                    pressureVector = [0] * len(nodeList)

                    for i in range(len(nodeList)):
                        for j in range(len(node._neighbourIDs)):
                            if (i == node._id):
                                pressureVector[i] = node._connections * node._initialPressure
                            elif (i == node._neighbourIDs[j]):
                                pressureVector[i] = -1 * node._initialPressure
                    
                    b.append((initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity)
                    A.append(pressureVector)
                    
                elif (node._sink == True and node._terminal == True):
                    pressureVector = [0] * len(nodeList)
                    
                    for i in range(len(nodeList)):
                        for j in range(len(node._neighbourIDs)):
                            if (i == node._id):
                                pressureVector[i] = node._connections * node._initialPressure
                            elif (i == node._neighbourIDs[j]):
                                pressureVector[i] = 0
                        
                    b.append(((len(nodeList) - 1) * initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity)
                    A.append(pressureVector)
                    
                elif (node._terminal == False):
                    pressureVector = [0] * len(nodeList)
                    
                    for i in range(len(nodeList)):
                        for j in range(len(node._neighbourIDs)):
                            if (i == node._id):
                                pressureVector[i] = node._connections * node._initialPressure
                            elif (i == node._neighbourIDs[j]):
                                pressureVector[i] = -1 * node._initialPressure
                    
                    b.append(0)
                    A.append(pressureVector)

            A = np.array(A)
            b = np.array(b)
            x = np.linalg.solve(A, b)
            
            for i in range(len(nodeList)):
                nodeList[i]._pressureVector.append(x[i])
            
            sinkNode._sink = False
    
    return


"""_summary_
Calculates the conductivity (D^t+1) throught each edge using equation (6)
"""
def calculateConductivity(currentNode, currentNeighbour, nodeListLength, edgeList, sigma, rho, tau, viscosity):
    
    pressureSum = 0
    for i in range(nodeListLength):
        pressureSum += currentNode._pressureVector[i] - currentNeighbour._pressureVector[i]
    
    kappa = 1 + sigma * (abs(pressureSum)) - rho
    
    
    
    for edge in currentNode._nodeEdgeList:
        if (currentNode._id == edge._start._id or currentNode._id == edge._end._id) and (currentNeighbour._id == edge._start._id or currentNeighbour._id == edge._end._id):
                edge._conductivity = edge._conductivity * kappa
                edge._radius = calculateRadius(edge, viscosity)
    
                if edge._conductivity < tau:
                    edgeList.remove(edge)
                    print("REMOVES! tau = " + str(tau))
        
    return


"""_summary_
Approximates the pressure change (p^t+1) for each node using equation (8)
"""
def calculatePressure(node, nodeList, initialFlow):
     
    for sinkNode in nodeList:
        sinkNode._sink = True
        
        for node in nodeList:
            
            index = 0

            if (node._sink == False and node._terminal == True):
            
                conductivitySum = 0
                conductivityPressureSum = 0
                
                for edge in node._nodeEdgeList:
                    if edge._start._id != node._id:
                        conductivityPressureSum += edge._conductivity * (edge._end._pressureVector[node._id] - edge._start._pressureVector[node._id])
                    if edge._end._id != node._id:
                        conductivityPressureSum += edge._conductivity * (edge._start._pressureVector[node._id] - edge._end._pressureVector[node._id])
                        
                    conductivitySum += edge._conductivity
                
                node._pressureVector[index] = ((initialFlow * node._nodeEdgeList[0]._length + conductivityPressureSum) / (2 * conductivitySum))
                
            elif (node._sink == True and node._terminal == True):
                for edge in node._nodeEdgeList:
                    node._pressureVector[index] = 0
                    
            if (node._terminal == False):
                conductivitySum = 0
                conductivityPressureSum = 0
                
                for edge in node._nodeEdgeList:
                    if edge._start._id != node._id:
                        conductivityPressureSum += edge._conductivity * (edge._end._pressureVector[node._id] - edge._start._pressureVector[node._id])
                    if edge._end._id != node._id:
                        conductivityPressureSum += edge._conductivity * (edge._start._pressureVector[node._id] - edge._end._pressureVector[node._id])
                        
                    conductivitySum += edge._conductivity
                
                node._pressureVector[index] = (conductivityPressureSum / (2 * conductivitySum))
                
            index += 1
            
        sinkNode._sink = False
        index = 0
        
    return

"""_summary_
Calculates radius of each edge, derived from equation (1)
"""
def calculateRadius(edge, viscosity):
    return ((edge._conductivity * 8 * viscosity) / np.pi) ** (1 / 4)


"""_summary_
Function is used to initialize the Physarium simulation by setting the initial conductivity and pressure
"""
def initializePhysarium(nodeList, edgeList, viscosity = 1.0, initialFlow = 10.0):
    initializeConductivity(edgeList, viscosity)
    initializePressure(nodeList, initialFlow)
    
    return
    

"""_summary_
Function is used to calculate each time step in the simulation
"""
def physarumAlgorithm(nodeList, edgeList, viscosity = 1.0, initialFlow = 10.0, sigma = 0.000000375, rho = 0.0002, tau = 0.0004):
    
    for node in nodeList:
        for neighbour in node._neighbour:
            calculateConductivity(node, neighbour, len(nodeList), edgeList, sigma, rho, tau, viscosity)
        calculatePressure(node, nodeList, initialFlow)

    return