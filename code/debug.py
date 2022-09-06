# -*- coding: utf-8 -*-

# Imports
import matplotlib.pyplot as plt

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
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/paper_graph.json"
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile)
    
    print("Number of nodes: " + str(numberOfNodes))
    print("Number of edges: " + str(numberOfEdges))
    
    # Slime parameters
    viscosity = 1.0
    initialFlow = 1.0
    sigma = 0.00000375
    rho = 0.0002
    tau = 0.0004
    edgeCost = 1
    
    environment = Environment()
    environment.createGrid(nodeList)
    environment.createTerminalNodes(nodeList)
    environment.createTerminalEdges(edgeList)    
    
    initializePhysarium(environment._edgeList, environment._nodeList, environment._terminalNodeList, environment._terminalEdgeList, viscosity, initialFlow)
    
    # Debugging
    # printInitialConductivity(environment._edgeList)
    # printInitialPressure(environment._nodeList)
   
    """
    fig = plt.figure(figsize = (10, 10), dpi = 200)
    ax = fig.add_subplot(111)
    fig = environment.plotGraph(plt)
    ax.set_title("Polycephalum Test, step = {}".format(1))
    plt.show()
    """
    
    for t in tqdm(range(1), desc = "Iteration progress"):
        
        physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau)
        
        #tau = 0.0004 * t
    
    #print(tau)
    
    # Debugging
    # printFlux(environment._edgeList)
    # printConductivity(environment._edgeList)
    # printEdgeRadius(environment._edgeList)
    # printPressure(environment._nodeList)
    
    return
    
if __name__ == "__main__":
    
    test()