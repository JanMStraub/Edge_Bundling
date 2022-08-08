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
                pressureList = list()
                
                for i in range(0, node._connections + 1):
                    if (i == node._id):
                        pressureList.extend([node._connections * node._initialPressure])
                    else:
                        pressureList.extend([-1 * node._initialPressure])
                    
                b.append((initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity)
                A.append(pressureList)
                
            elif (node._sink == True):
                pressureList = list()
                
                for i in range(0, node._connections + 1):
                    if (i == node._id):
                        pressureList.extend([node._connections * node._initialPressure])
                    else:
                        pressureList.extend([0])
                    
                b.append(((len(nodeList) - 1) * initialFlow * node._nodeEdgeList[0]._length) / node._nodeEdgeList[0]._conductivity)
                A.append(pressureList)
                
            else:
                pressureList = list()
                
                for i in range(0, node._connections + 1):
                    if (i == node._id):
                        pressureList.extend([node._connections * node._initialPressure])
                    else:
                        pressureList.extend([-1 * node._initialPressure])
                
                b.append(0)
                A.append(pressureList)
                
        A = np.array(A)
        b = np.array(b)
        x = np.linalg.solve(A, b)
        
        for i in range(len(nodeList)):
            nodeList[i]._initialPressure = x[i]
            nodeList[i]._pressureVector.append(x[i])
        
        sinkNode._sink = False
    
    return


"""_summary_
Calculates the flux (Q^t) throught each edge using equation (5)
"""
def calculateFlux(nodeList, edgeList):
    for edge in edgeList:
        pressureSum = 0
        for i in range(0, len(nodeList)):
            pressureSum += edge._start._pressureVector[i] - edge._end._pressureVector[i]
        edge._flux = (edge._conductivity / edge._length) * pressureSum
    
    return


"""_summary_
Calculates the conductivity (D^t+1) throught each edge using equation (6)
"""
def calculateConductivity(edgeList, sigma, rho):
    for edge in edgeList:
        edge._conductivity = edge._conductivity + (sigma * abs(edge._flux - rho * edge._cost * edge._conductivity))
    
    return


"""_summary_
Approximates the pressure change (p^t+1) for each node using equation (8)
"""
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

    return