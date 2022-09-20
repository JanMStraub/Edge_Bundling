# -*- coding: utf-8 -*-

# Imports
from tqdm import tqdm

from environment import Environment
from helper import readGraphData
from simulation import physarumAlgorithm, initializePhysarium, updateCalculations

"""_summary_
Prints the initial conductivity for each node
"""
def printInitialConductivity(edgeList):
    for edge in edgeList:
                
        print("Initial conductivity of edge {}: {}".format(edge._id, edge._conductivity[0]))
    
    print("\n####################################################################\n")
    
    return


"""_summary_
Prints the initial pressure for each node
"""
def printInitialPressure(nodeList):
    for node in nodeList:
        print("Initial pressure for node {}: {}".format(node._id, node._currentPressureVector))
        
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
        print("Conductivity of edge {}: {}".format(edge._id, edge._conductivity[1]))
        
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
        if node._terminal == True:
            print("Pressure for terminal node {}: {}".format(node._id, node._currentPressureVector))
        else:
            print("Pressure for node {}:          {}".format(node._id, node._currentPressureVector))  
        
    print("\n####################################################################\n")
    
    return


def checkGrid(edgeList, nodeList):
    
    for edge in edgeList:
        print("Edge ID: {} - start: {} - end: {}".format(edge._id, edge._start._id, edge._end._id))
    
    print("\n####################################################################\n")
    
    for node in nodeList:
        print("Node ID: {} - neighbours: {} - neighbour IDs: {}".format(node._id, len(node._neighbours), node._neighbourIDs))
    
    print("\n####################################################################\n")
    
    for node in nodeList:
        for edge in node._nodeEdgeList:
            print("node ID: {} - edge ID: {} - start: {} - end: {}".format(node._id, edge._id, edge._start._id, edge._end._id))
        print("\n####################################################################\n")
    
    return


def printEdgeCost(edgeList):
    for edge in edgeList:
        print("Edge ID: {} - cost: {}".format(edge._id, edge._cost))
        
    print("\n####################################################################\n")
    
    
def printEdgePosition(edgeList):
    for edge in edgeList:
        print("Edge ID: {} - Start position: {} - End position: {}".format(edge._id, edge._start._position, edge._end._position))
        
    print("\n####################################################################\n")
    
    
def printNodeConnections(nodeList):
    for node in nodeList:
        print("Node ID: {} - connections: {}".format(node._id, node._connections))
    
    print("\n####################################################################\n")


"""_summary_
Function exits only for testing purposes
""" 
def test(jsonFile, steps, viscosity, initialFlow, sigma, rho, tau):     
    
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile)
    
    print("Number of nodes: " + str(numberOfNodes))
    print("Number of edges: " + str(numberOfEdges))
    
    environment = Environment()
    environment.createGrid(nodeList)
    environment.createTerminalNodes(nodeList)
    # environment.createTerminalEdges(nodeList, edgeList, edgeCost)    
    
    initializePhysarium(environment._edgeList, environment._nodeList, environment._terminalNodeList, viscosity, initialFlow)

    # Debugging
    printNodeConnections(environment._nodeList)
    # checkGrid(environment._edgeList, environment._nodeList)
    # printEdgePosition(environment._edgeList)
    # printEdgeCost(environment._edgeList)
    # printInitialConductivity(environment._edgeList)
    # printInitialPressure(environment._nodeList)
    
    print()    
    
    for t in tqdm(range(steps), desc = "Iteration progress"):
        
        physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau)
        
        updateCalculations(environment._edgeList, environment._nodeList)
        
        tau = 0.0004 * t
        
    print()

    # Debugging
    # printFlux(environment._edgeList)
    printConductivity(environment._edgeList)
    # printEdgeRadius(environment._edgeList)
    printPressure(environment._nodeList)
    printNodeConnections(environment._nodeList)
    
    return