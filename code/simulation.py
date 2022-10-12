# -*- coding: utf-8 -*-

# Imports
from os import remove, terminal_size
import random

import numpy as np

from tqdm import tqdm

from helper import findOtherEdgeEnd


"""_summary_
Initializes the conductivity (D_0) of all edges according to equation (1)
"""
def initializeConductivity(edge, viscosity):
    edge._conductivity[0] = edge._conductivity[1] = (np.pi * edge._radius ** 4) / (8 * viscosity)
    
    return


"""_summary_
Calculates radius of each edge, derived from equation (1)
"""
def calculateRadius(edge, viscosity):
    return ((edge._conductivity[1] * 8 * viscosity) / np.pi) ** (1 / 4)


def chooseSinkAndSource(terminalNodeList):
    
    l = []
    probability = [0]
    T = len(terminalNodeList) - 1
    edgeCostSum = 0
    spaceing = 0
    
    for terminal in terminalNodeList:
        totalEdgeCost = 0
        for edge in terminal._nodeEdgeList:
            totalEdgeCost += edge._cost

        terminal._totalEdgeCost = totalEdgeCost
        edgeCostSum += totalEdgeCost
        l.append(terminal)
        
    l.sort(key = lambda terminal: terminal._totalEdgeCost)

    for i in range(len(terminalNodeList)):
        spaceing += l[T - i]._totalEdgeCost / edgeCostSum
        probability.append(spaceing)
    
    sinkSelector = random.uniform(0, 1)

    for i in range(len(probability)):
        if (probability[i] < sinkSelector and probability[i + 1] >= sinkSelector):
            l[i]._sink = True   
            print("SINK node: {}".format(l[i]._id))    

    return


def calculatePressure(nodeList, terminalNodeList, initialFlow):
    A = list()            
    b = list()

    for node in nodeList:
        if (node._sink == False and node._terminal == True):
            pressureVector = [0] * len(nodeList)
            nodeFactor = 0
            for edge in node._nodeEdgeList:
                neighbour = findOtherEdgeEnd(node, edge)
                neighbourFactor = edge._conductivity[0] / edge._compositeCost
                nodeFactor -= neighbourFactor
                pressureVector[neighbour._id] = neighbourFactor
            pressureVector[node._id] = nodeFactor     
                
            b.append(-1 * initialFlow)
            A.append(pressureVector)             
        
        elif (node._sink == True and node._terminal == True):
            pressureVector = [0] * len(nodeList)
            nodeFactor = 0
            for edge in node._nodeEdgeList:
                neighbour = findOtherEdgeEnd(node, edge)
                neighbourFactor = edge._conductivity[0] / edge._compositeCost
                nodeFactor -= neighbourFactor
                pressureVector[neighbour._id] = neighbourFactor
            pressureVector[node._id] = nodeFactor       
            b.append((len(terminalNodeList) - 1) * initialFlow)
            
            A.append(pressureVector)
            node._sink = False
        
        elif (node._sink == False and node._terminal == False):
            pressureVector = [0] * len(nodeList)
            nodeFactor = 0
            for edge in node._nodeEdgeList:
                neighbour = findOtherEdgeEnd(node, edge)
                neighbourFactor = edge._conductivity[0] / edge._compositeCost
                nodeFactor -= neighbourFactor
                pressureVector[neighbour._id] = neighbourFactor
            pressureVector[node._id] = nodeFactor       
            
            b.append(0)
            A.append(pressureVector)
        
        else:
            raise ValueError("Something went wrong with the grid creation")
          
    for entry in A:
        print(entry)
    print(b)
    print("###################################")
    
    A = np.array(A)
    b = np.array(b)

    x = np.linalg.solve(A, b)
    
    for i in range(len(nodeList)):
        nodeList[i]._pressure = x[i]

    return
        

def calculateCompositeCost(edge, maxNodeWeight):
    edge._compositeCost = edge._cost - (edge._start._weight / edge._start._connections) - (edge._end._weight / edge._end._connections) + 2 * maxNodeWeight
    
    return 


def calculateFlux(edgeList, maxNodeWeight):
    for edge in edgeList:
        calculateCompositeCost(edge, maxNodeWeight)
        edge._flux = (edge._conductivity[0] / edge._compositeCost) * (edge._start._pressure - edge._end._pressure)
    
    return


def f(x, alpha):
    return alpha * x
    
    
def updateConductivities(edgeList, mu, alpha):
    for edge in edgeList:
        edge._conductivity[1] = edge._alpha * (edge._conductivity[0] + f(abs(edge._flux), alpha) - mu * edge._conductivity[0])
        
    return
    

def calculateTotalCost(edgeList):
    totalEdgeCost = 0
    
    for edge in edgeList:
        totalEdgeCost += edge._cost
        
    return totalEdgeCost


"""_summary_
Function is used to calculate each time step in the simulation
"""
def physarumAlgorithm(nodeList, terminalNodeList, edgeList, viscosity, initialFlow, mu, epsilon, K, alpha):
    maxNodeWeight = 0
       
    for node in nodeList:
        if (node._weight > maxNodeWeight):
            maxNodeWeight = node._weight 
            
    for edge in edgeList:
        initializeConductivity(edge, viscosity)  
        calculateCompositeCost(edge, maxNodeWeight) 

    for k in tqdm(range(K), desc = "Inner iteration progress"):

        chooseSinkAndSource(terminalNodeList)
        calculatePressure(nodeList, terminalNodeList, initialFlow)        
        calculateFlux(edgeList, maxNodeWeight)
        updateConductivities(edgeList, mu, alpha)
        
        for edge in edgeList:
            # edge cutting
            if edge in edgeList and edge._conductivity[1] < epsilon:
                
                print("REMOVED Edge: {}".format(edge._id))
                
                edge._start._nodeEdgeList.remove(edge)
                edge._end._nodeEdgeList.remove(edge)
                
                edge._start._connections -= 1
                edge._end._connections -= 1
                
                edge._start._neighbours.remove(edge._end)
                edge._end._neighbours.remove(edge._start)
                
                edge._start._neighbourIDs.remove(edge._end._id)
                edge._end._neighbourIDs.remove(edge._start._id)
                
                edgeList.remove(edge)
                
            else:
                edge._conductivity[0] = edge._conductivity[1]
        
        totalEdgeCost = calculateTotalCost(edgeList)

    return totalEdgeCost