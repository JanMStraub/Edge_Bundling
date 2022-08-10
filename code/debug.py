# -*- coding: utf-8 -*-

# Imports
from environment import Environment
from helper import readGraphData
from simulation import physarumAlgorithm, initializePhysarium


"""_summary_
Prints the initial conductivity for each node
"""
def printInitialConductivity(edgeList):
    for edge in edgeList:
                
        print("Initial conductivity of edge {}: {}".format(edge._id, edge._conductivity))
    
    print("\n####################################################################\n")
    
    return


"""_summary_
Prints the initial pressure for each node
"""
def printInitialPressure(nodeList):
    for node in nodeList:
        print("Initial pressure for node {}: {}".format(node._id, node._pressureVector[0]))
        
    print("\n####################################################################\n")
    
    return


"""_summary_
Prints the flux at each edge
"""
def printFlux(edgeList):
    for edge in edgeList:
        print("Flux of edge {}: {}".format(edge._id, edge._flux))
        
    print("\n####################################################################\n")
    
    return


"""_summary_
Prints the conductivity at each edge
"""
def printConductivity(edgeList):
    for edge in edgeList:
        print("Conductivity of edge {}: {}".format(edge._id, edge._conductivity))
        
    print("\n####################################################################\n")   
    return


"""_summary_
Prints the pressure for each node
"""
def printPressure(nodeList):
    for node in nodeList:
        print("Pressure for node {}: {}".format(node._id, node._pressureVector))
        
    print("\n####################################################################\n")
    
    return


"""_summary_
Function exits only for testing purposes
""" 
def test():
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/test_graph.json"
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile)
     
    environment = Environment(200, 200)
    environment.createNodes(nodeList)
    environment.createEdges(edgeList, 1)
    
    
    initializePhysarium(environment._nodeList, environment._edgeList, viscosity = 1.0, initialFlow = 10.0)
    
    # Debugging
    printInitialConductivity(environment._edgeList)
    printInitialPressure(environment._nodeList)
   
    physarumAlgorithm(environment._nodeList, environment._edgeList, 1.0, 10.0, 0.1, 0.2) # 0.000000375, 0.0002
    
    # Debugging
    printFlux(environment._edgeList)
    printConductivity(environment._edgeList)
    printPressure(environment._nodeList)
    
    
    return
    
if __name__ == "__main__":
    
    test()