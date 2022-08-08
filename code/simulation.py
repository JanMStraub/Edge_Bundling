# -*- coding: utf-8 -*-

# Imports
import numpy as np

from environment import Environment
from helper import readGraphData, calculateFlux, initializeConductivity, calculateConductivity, calculatePressure

    
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