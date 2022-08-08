# -*- coding: utf-8 -*-

# Imports
import numpy as np

from environment import Environment
from helper import readGraphData, calculateFlux, initializeConductivity, calculateConductivity, calculatePressure

    
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
    

def physarumOptimizationAlgorithm(nodeList, edgeList, viscosity = 1.0, initialFlow = 10.0, sigma = 0.000000375, rho = 0.0002):
    initializeConductivity(edgeList, viscosity)
    
    for node in nodeList:
        node._sink = True
        initializePressure(nodeList, initialFlow)
        print("ID: {}, pressure: {}".format(node._id, node._pressure))
        node._sink = False
    
    calculateFlux(nodeList, edgeList)
    calculateConductivity(edgeList, sigma, rho)
    
    for ndoe in nodeList:
        calculatePressure(node, edgeList, initialFlow)
    

    return
            
    
# only for testing   
def test():
    jsonFile = "code/data/simple_graph.json"
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile)
     
    environment = Environment(200, 200)
    environment.createNodes(nodeList)
    environment.createEdges(edgeList)
   
    physarumOptimizationAlgorithm(environment._nodeList, environment._edgeList, 1.0, 10.0, 0.000000375, 0.0002)

    return
    
if __name__ == "__main__":
    
    test()