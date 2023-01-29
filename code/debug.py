6# -*- coding: utf-8 -*-

# Imports
from tqdm import tqdm
from sys import maxsize
from concurrent.futures import ProcessPoolExecutor, as_completed
from environment import ENVIRONMENT
from helper import read_graph_data, get_min_max_values, minimum_spanning_tree_length
from simulation import physarum_algorithm

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
            print("Pressure for terminal node {}: {}".format(node._id, node._pressure))
        else:
            print("Pressure for          node {}: {}".format(node._id, node._pressure))  
        
    print("\n####################################################################\n")
    
    return


"""_summary_
    Prints all grid nodes and edges to check if they connect
"""
def checkGrid(edgeList, nodeList):
    
    for edge in edgeList:
        print("Edge ID: {} - start: {} - end: {}".format(edge._id, edge._start._id, edge._end._id))
    
    print("\n####################################################################\n")
    
    for node in nodeList:
        neighbourIDs = []
        
        for neighbour in node._neighbours:
            neighbourIDs.append(neighbour._id)
        
        print("Node ID: {} - neighbours: {} - neighbour IDs: {}".format(node._id, len(node._neighbours), neighbourIDs))
    
    print("\n####################################################################\n")
    
    for node in nodeList:
        for edge in node._nodeEdgeList:
            print("node ID: {} - edge ID: {} - start: {} - end: {}".format(node._id, edge._id, edge._start._id, edge._end._id))
        print("\n####################################################################\n")
    
    return


"""_summary_
    Function prints edge cost
"""
def printEdgeCost(edgeList):
    for edge in edgeList:
        print("Edge ID: {} - cost: {}".format(edge._id, edge._cost))
        
    print("\n####################################################################\n")

    return
    

"""_summary_
    Function prints edge position
"""
def printEdgePosition(edgeList):
    for edge in edgeList:
        print("Edge ID: {} - Start position: {} - End position: {}".format(edge._id, edge._start._position, edge._end._position))
        
    print("\n####################################################################\n")
    
    return
    

"""_summary_
    Prints node connections
"""
def printNodeConnections(nodeList):
    for node in nodeList:
        print("Node ID: {} - connections: {}".format(node._id, node._connections))
    
    print("\n####################################################################\n")
    
    return
   
    
"""_summary_
    Prints node weights
""" 
def printNodeWeight(nodeList):
    for node in nodeList:
        print("Node ID: {} - weight: {}".format(node._id, node._weight))
    
    print("\n####################################################################\n")
    
    return
    

def start(nodeList,
        xMin,
        xMax,
        yMin,
        yMax,
        viscosity,
        initialFlow,
        mu,
        epsilon,
        innerIteration,
        alpha,
        edgeAlpha):
    
    # Setup environment
    environment = ENVIRONMENT(
        nodeList,
        xMin,
        xMax,
        yMin,
        yMax,
        viscosity)
    
    totalCost, steinerConnections = physarum_algorithm(
        environment.environmentNodeList,
        environment.environmentTerminalNodeList,
        environment.environmentEdgeList,
        initialFlow,
        mu,
        epsilon,
        innerIteration,
        alpha,
        edgeAlpha)

    return totalCost, steinerConnections, environment



"""_summary_
    Function exits only for testing purposes
""" 
def test(jsonFile, viscosity, initialFlow, mu, epsilon, alpha, edgeAlpha):     
    
    # Import graph information from JSON
    nodeList, pathList = read_graph_data(jsonFile)
    xMin, xMax, yMin, yMax = get_min_max_values(nodeList)
    bestCostList = [maxsize] #[minimum_spanning_tree_length(nodeList, pathList)]
    xAxis, yAxis = int((xMax - xMin) + 1), int((yMax - yMin) + 1)

    # Outer and inner iteration bound
    if xAxis >= yAxis:
        outerIteration = xAxis ** 2
        innerIteration = xAxis ** 2 * 10
    elif xAxis < yAxis:
        outerIteration = yAxis ** 2
        innerIteration = yAxis ** 2 * 10

    outerIteration = 30
    innerIteration = 1000

    print(f"xAxis: {xAxis} - "
          f"yAxis: {yAxis} - "
          f"outerIteration: {outerIteration} - "
          f"innerIteration: {innerIteration}")
       
    # Debugging
    # printNodeConnections(environment._nodeList)
    # checkGrid(environment._edgeList, environment._nodeList)
    # printEdgePosition(environment._edgeList)
    # printEdgeCost(environment._edgeList)
    # printInitialConductivity(environment._edgeList)
    # printInitialPressure(environment._nodeList)
    # printNodeWeight(environment._nodeList)

    savedNetwork = None
    results = None
    
    with ProcessPoolExecutor() as executor:

        # Start simulation
        results = [executor.submit(start,
                                    nodeList,
                                    xMin,
                                    xMax,
                                    yMin,
                                    yMax,
                                    viscosity,
                                    initialFlow,
                                    mu,
                                    epsilon,
                                    innerIteration,
                                    alpha,
                                    edgeAlpha) for _ in tqdm(range(outerIteration), desc = "Outer iteration progress")]
        
        for item in as_completed(results):
            totalCost, steinerConnections, environment = item.result()
            if bestCostList[-1] >= totalCost and steinerConnections:
                savedNetwork = environment
                bestCostList.append(totalCost)
    
    # Saveguard if no network is found yet
    if savedNetwork == None:
        outerIteration += 1

    # Debugging
    # printFlux(environment._edgeList)
    # printConductivity(environment._edgeList)
    # printEdgeRadius(environment._edgeList)
    # printPressure(environment._nodeList)
    # printNodeConnections(environment._nodeList)
    # printEdgeCost(environment._edgeList)
