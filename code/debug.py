# -*- coding: utf-8 -*-

# Imports
import math

from tqdm import tqdm

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
        print("Initial pressure for node {}: {}".format(node._id, node._pressureVector))
        
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
Prints the radius of each edge
"""
def printEdgeRadius(edgeList):
    for edge in edgeList:
         print("Radius of edge {}: {}".format(edge._id, edge._radius))
        
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
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/simple_graph.json"
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile)
    
    print("Number of nodes: " + str(numberOfNodes))
    print("Number of edges: " + str(numberOfEdges))
    
    # Slime parameters
    viscosity = 1.0
    initialFlow = 0.5
    sigma = 0.00000375
    rho = 0.0002
    tau = 0.0004
    edgeCost = 1
    
    environment = Environment()
    environment.createNodes(nodeList)
    environment.createEdges(edgeList, edgeCost)
    
    initializePhysarium(environment._nodeList, environment._edgeList, viscosity, initialFlow)
    
    # Debugging
    printInitialConductivity(environment._edgeList)
    printInitialPressure(environment._nodeList)
   
    for t in tqdm(range(50000), desc = "Iteration progress"):
        
        physarumAlgorithm(environment._nodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau)
        
        tau = 0.0004 * t
        
    print(tau)
    
    # Debugging
    # printFlux(environment._edgeList)
    # printConductivity(environment._edgeList)
    # printEdgeRadius(environment._edgeList)
    # printPressure(environment._nodeList)
    
    return
    
if __name__ == "__main__":
    
    test()