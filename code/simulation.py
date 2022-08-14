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
        sinkNode._sink = True
        
        A = list()
        b = list()
        
        for node in nodeList:

            if (node._sink == False):
                pressureVector = [0] * len(nodeList)

                for i in range(len(nodeList)):
                    for j in range(len(node._neighbourIDs)):
                        if (i == node._id):
                            pressureVector[i] = node._connections * node._initialPressure
                        elif (i == node._neighbourIDs[j]):
                            pressureVector[i] = -1 * node._initialPressure
                
                b.append((initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity)
                A.append(pressureVector)
                
            elif (node._sink == True):
                pressureVector = [0] * len(nodeList)
                
                for i in range(len(nodeList)):
                    for j in range(len(node._neighbourIDs)):
                        if (i == node._id):
                            pressureVector[i] = node._connections * node._initialPressure
                        elif (i == node._neighbourIDs[j]):
                            pressureVector[i] = 0
                    
                b.append(((len(nodeList) - 1) * initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity)
                A.append(pressureVector)
                
            else:
                pressureVector = [0] * len(nodeList)
                
                for i in range(node._connections + 1):
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
Calculates the flux (Q^t) throught each edge using equation (5)
"""
def calculateFlux(nodeList, edgeList):
    for edge in edgeList:
        pressureSum = 0
        for i in range(len(nodeList)):
            pressureSum += edge._start._pressureVector[i] - edge._end._pressureVector[i]
        edge._flux = (edge._conductivity / edge._length) * pressureSum
    
    return


"""_summary_
Calculates the conductivity (D^t+1) throught each edge using equation (6)
"""
def calculateConductivity(edgeList, sigma, rho):
    for edge in edgeList:
        edge._conductivity = edge._conductivity + (sigma * abs(edge._flux) - rho * edge._cost * edge._conductivity)
    
    return


"""_summary_
Approximates the pressure change (p^t+1) for each node using equation (8)
"""
def calculatePressure(nodeList, initialFlow):
     
    for sinkNode in nodeList:
        sinkNode._sink = True
        
        for node in nodeList:

            if (node._sink == False):
                
                conductivitySum = 0
                conductivityPressureSum = 0
                
                for edge in node._nodeEdgeList:
                    if edge._start._id != node._id:
                        conductivityPressureSum += edge._conductivity * edge._start._pressureVector[node._id]
                    if edge._end._id != node._id:
                        conductivityPressureSum += edge._conductivity * edge._end._pressureVector[node._id]
                        
                    conductivitySum += edge._conductivity
                
                node._pressureVector.append((initialFlow * node._nodeEdgeList[0]._length + conductivityPressureSum) / conductivitySum)
                
            elif (node._sink == True):
                for edge in node._nodeEdgeList:
                    node._pressureVector.append(0)
                    
            else:
                conductivitySum = 0
                conductivityPressureSum = 0
                
                for edge in node._nodeEdgeList:
                    if edge._start._id != node._id:
                        conductivityPressureSum += edge._conductivity * edge._start._pressureVector[node._id]
                    if edge._end._id != node._id:
                        conductivityPressureSum += edge._conductivity * edge._end._pressureVector[node._id]
                        
                    conductivitySum += edge._conductivity
                
                node._pressureVector.append(conductivityPressureSum / conductivitySum)
            
        sinkNode._sink = False
        
    return


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
def physarumAlgorithm(nodeList, edgeList, viscosity = 1.0, initialFlow = 10.0, sigma = 0.000000375, rho = 0.0002):

    calculateFlux(nodeList, edgeList)
    calculateConductivity(edgeList, sigma, rho)
    calculatePressure(nodeList, initialFlow)

    return