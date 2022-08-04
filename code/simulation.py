# -*- coding: utf-8 -*-

# Imports
import random

import numpy as np

from environment import Environment
from helper import readGraphData, calculateFlux


def calculateFlow(nodeList, edgeList, viscosity):
    source, sink = random.sample(nodeList, 2)
    
    source._flux = 10
    sink._pressure = 0
    

    queue = []
    queue.append(sink)
    
    while queue:
        print(len(queue))
        currentNode = queue.pop(0)
        
        if currentNode == source:
            for node in nodeList:
                print("ID: {}, pressure: {}".format(node._id, node._pressure))
                node._visited = False
            return
        
        for edge in currentNode.nodeEdgeList:
            
            #calculatePressure(viscosity, edge, currentNode, source, sink)
            calculateFlux(viscosity, edge)
            
            if((edge._start != currentNode) and (edge._start._visited == False)):
                queue.append(edge._start)
            
            if((edge._end != currentNode) and (edge._end._visited == False)):
                queue.append(edge._end)
        
        currentNode._visited = True     
    
    return


def initializeConductivity(edgeList, viscosity):
    for entry in edgeList:
        entry._conductivity = (np.pi * entry._radius ** 4) / (8 * viscosity)
    
    return

    
def initializePressure(nodeList, initialFlow):
    A = list()
    b = list()
    
    for entry in nodeList:
        
        if (entry._sink == False):
            pressureList = list()
            
            for i in range(0, entry._connections + 1):
                if (i == entry._id):
                    pressureList.extend([entry._connections])
                else:
                    pressureList.extend([-1])
                
            b.append((initialFlow) / entry._nodeEdgeList[0]._conductivity) # (initialFlow * edge._length)
            A.append(pressureList)
            
        elif (entry._sink == True):
            pressureList = list()
            
            for i in range(0, entry._connections + 1):
                if (i == entry._id):
                    pressureList.extend([entry._connections])
                else:
                    pressureList.extend([0])
                
            b.append(((len(nodeList) - 1) * initialFlow) / entry._nodeEdgeList[0]._conductivity) # (len(nodeList) - 1) * initialFlow * edge._length)
            A.append(pressureList)
        else:
            pressureList = list()
            
            for i in range(0, entry._connections + 1):
                if (i == entry._id):
                    pressureList.extend([entry._connections])
                else:
                    pressureList.extend([-1])
            
            b.append(0)
            A.append(pressureList)
            
    A = np.array(A)
    b = np.array(b)
    x = np.linalg.solve(A, b)
    
    for i in range(len(nodeList)):
        nodeList[i]._pressure = x[i]
    
    for entry in nodeList:
        print(entry._sink)
        print(entry._pressure)
    
    return
    

def physarumOptimizationAlgorithm(nodeList, edgeList, viscosity, initialFlow):
    randomNode = random.choice(nodeList)
    randomNode._sink = True
    initializeConductivity(edgeList, viscosity)
    initializePressure(nodeList, initialFlow)

    return
            
    
# only for testing   
def test():
    jsonFile = "code/data/simple_graph.json"
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile)
     
    environment = Environment(200, 200)
    environment.createNodes(nodeList)
    environment.createEdges(edgeList)
    
    # calculateFlow(environment._nodeList, environment._edgeList, 4.5)
    physarumOptimizationAlgorithm(environment._nodeList, environment._edgeList, 1.0, 10.0)

    return
    
if __name__ == "__main__":
    
    test()