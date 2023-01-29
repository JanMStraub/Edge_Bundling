# -*- coding: utf-8 -*-

"""
Main approximation file
@author: Jan Straub
"""

# Imports
from random import uniform
from numpy.linalg import lstsq
from numpy import zeros
from numba import jit
from time import localtime, strftime

from helper import find_other_edge_end


def initialize_composite_cost(edge, maxNodeWeight):

    """_summary_
        Initializes composite cost using equation (4)
    Args:
        edge (object): Edge object
        maxNodeWeight (float): Max node weight of all nodes in nodeList

    Returns:
        compositeCost (float): Composite cost of the node
    """

    startWeightConnections = edge.start.weight / edge.start.connections
    endWeightConnections = edge.end.weight / edge.end.connections
    compositeCost = edge.cost - startWeightConnections - endWeightConnections + 2 * maxNodeWeight
    edge.compositeCost = compositeCost

    return compositeCost


def calculate_neighbour_factor(edge, compositeCost):

    """_summary_
        Calculate neighbour factor
    Args:
        edge (object): Edge object
        compositeCost (float): The composite cost of the node
    """

    edge.neighbourFactor = edge.conductivity[0] / compositeCost


def choose_sink_and_source(terminalNodeList, terminalNodeListLength):

    """_summary_
        Uses the probability equation (7) to select a node
        from the terminal node list to become the sink
    Args:
        terminalNodeList (list): List of terminal node objects
        terminalNodeListLength (int): Length of terminalNodeList

    Returns:
        choosenSink (object): Sink node object
    """

    terminalList, probability = [], [0]
    edgeCostSum, spaceing = 0, 0
    choosenSink = None
    terminalListAppend, probabilityAppend = terminalList.append, probability.append

    for terminal in terminalNodeList:
        totalEdgeCost = 0
        for edge in terminal.nodeEdgeList:
            totalEdgeCost += edge.cost

        terminal.totalEdgeCost = totalEdgeCost
        edgeCostSum += totalEdgeCost
        terminalListAppend(terminal)

    terminalList.sort(key = lambda terminal: terminal.totalEdgeCost)

    for i in range(terminalNodeListLength):
        spaceing += terminalList[terminalNodeListLength - 1 - i].totalEdgeCost / edgeCostSum
        probabilityAppend(spaceing)

    sinkSelector = uniform(0, 1)

    for i, node in enumerate(probability):
        if node < sinkSelector <= probability[i + 1]:
            terminalList[i].sink = True
            choosenSink = terminalList[i]

    return choosenSink

@jit
def solve_l_g_s(pressureMatrix, flowVector):

    """_summary_
        Solves LGS
    Args:
        pressureMatrix (np.array): 2D pressure array
        flowVector (np.array): flow vector

    Returns:
        solvedLGS (np.array): Solved LGS with sparce solver or least squares
    """

    return lstsq(pressureMatrix, flowVector)[0]


def calculate_pressure(nodeList, terminalNodeList, initialFlow,
                       sinkNode, maxNodeWeight):

    """_summary_
        Calculates pressure at each node using equation (8)
    Raises:
        ValueError: If the grid creation went wrong
    """

    nodeListLength = len(nodeList)
    pressureMatrix, flowVector = zeros([nodeListLength, nodeListLength]), zeros(nodeListLength)

    for pos, node in reversed(list(enumerate(nodeList))):

        if node.connections == 0:
            pressureMatrix[pos] = zeros(nodeListLength)

        elif not node.sink and node.terminal:
            flowVector[pos] = -1 * initialFlow
            pressureMatrix[pos] = build_pressure_vector(nodeListLength,
                                                        nodeList, sinkNode,
                                                        node, pos)

        elif node.sink and node.terminal:
            flowVector[pos] = (len(terminalNodeList) - 1) * initialFlow
            pressureMatrix[pos] = build_pressure_vector(nodeListLength,
                                                        nodeList, sinkNode,
                                                        node, pos)
            node.sink = False

        elif not node.sink and not node.terminal:
            pressureMatrix[pos] = build_pressure_vector(nodeListLength,
                                                        nodeList, sinkNode,
                                                        node, pos)

        else:
            raise ValueError("Something went wrong with the grid creation")

        if node.connections != 0 and node.weight > maxNodeWeight:
            maxNodeWeight = node.weight

    solvedLGS = solve_l_g_s(pressureMatrix, flowVector)

    for pos, node in reversed(list(enumerate(nodeList))):
        node.pressure = solvedLGS[pos]
        if node.connections == 0:
            nodeList.remove(node)
            del node


def build_pressure_vector(nodeListLength,
                          nodeList, sinkNode,
                          node, pos):

    """_summary_
        Function builds pressure vector
    Returns:
        pressureVector (np.array): The current pressure vector
    """

    pressureVector = zeros(nodeListLength)
    nodeFactor = 0

    for edge in node.nodeEdgeList:
        neighbour = find_other_edge_end(node, edge)
        neighbourIndex = nodeList.index(neighbour)
        nodeFactor += edge.neighbourFactor
        pressureVector[neighbourIndex] = edge.neighbourFactor

    if pos != nodeList.index(sinkNode):
        pressureVector[pos] = -1 * nodeFactor

    return pressureVector


def calculate_flux(edge, oldConductivity):

    """_summary_
        Calculates the flux using equation (3)
    Args:
        edge (object): Edge object
        oldConductivity (float): Old edge conductivity

    Returns:
        flux (float): Current flux through edge
    """

    return (oldConductivity / edge.compositeCost) * (edge.start.pressure - edge.end.pressure)


def update_conductivities(edge, mu, alpha, edgeAlpha,
                          oldConductivity, edgeFlux):

    """_summary_
        Updates edge conductivity by using equation (9)
    Args:
        edge (object): Edge object
        mu (int): A constant
        alpha (float): A positiv constant
        edgeAlpha (float): A positiv constant for each edge
        oldConductivity (float): Old edge conductivity
        edgeFlux (float): Current flux through edge
    """

    edge.conductivity[1] = edgeAlpha * (oldConductivity + alpha * edgeFlux -
                                        mu * oldConductivity)


def physarum_algorithm(nodeList, terminalNodeList, edgeList,
                      initialFlow, mu, epsilon,
                      innerIteration, alpha, edgeAlpha,
                      outerIter):

    """_summary_
        Function controls physarium algorithm
    Args:
        nodeList (list): List of node objects
        terminalNodeList (list): List of terminal node objects
        edgeList (list): List of edge objects
        initialFlow (float): The initial flow of the fluid
        mu (int): A constant
        epsilon (float): Coductivity threshold
        innerIteration (int): Number of inner iterations
        alpha (float): A positiv constant
        edgeAlpha (float): A positiv constant for each edge

    Returns:
        totalEdgeCost (float): Total cost of the network
        steinerConnections (bool): If only Steiner connections are present
    """

    maxNodeWeight, totalEdgeCost, breakCounter = 0, 0, 0
    steinerConnections = True
    terminalNodeListLength = len(terminalNodeList)
    nodeListLength = len(nodeList)

    # Initialization
    for edge in edgeList:
        compositeCost = initialize_composite_cost(edge, maxNodeWeight)

        calculate_neighbour_factor(edge, compositeCost)

    for innerIter in range(innerIteration):

        sinkNode = choose_sink_and_source(terminalNodeList,
                                          terminalNodeListLength)

        calculate_pressure(nodeList, terminalNodeList, initialFlow,
                          sinkNode, maxNodeWeight)

        modifiableEdgeList, edgeListLength = edgeList, len(edgeList)

        for edge in edgeList:
            oldConductivity = edge.conductivity[0]
            calculate_flux(edge, maxNodeWeight)

            update_conductivities(edge, mu, alpha, edgeAlpha, oldConductivity,
                                  abs(calculate_flux(edge, oldConductivity)))

            # edge cutting
            if edge.conductivity[1] < epsilon and edge in modifiableEdgeList and edge in edgeList:

                edge.start.nodeEdgeList.remove(edge)
                edge.end.nodeEdgeList.remove(edge)

                edge.start.connections -= 1
                edge.end.connections -= 1

                edge.start.neighbours.remove(edge.end)
                edge.end.neighbours.remove(edge.start)

                modifiableEdgeList.remove(edge)
                del edge

            else:
                edge.conductivity[0] = edge.conductivity[1]
                calculate_neighbour_factor(edge, edge.compositeCost)

        if len(edgeList) == edgeListLength:
            breakCounter += 1

        edgeList = modifiableEdgeList

        # Check for early inner iteration stop
        if breakCounter > nodeListLength:
            checkTerminal = True
            breakCounter = 0
            for terminal in terminalNodeList:
                if terminal.connections != 1:
                    checkTerminal = False

            if checkTerminal:
                for edge in edgeList:
                    totalEdgeCost += edge.cost
                    if edge.start.connections > 3:
                        steinerConnections = False

                endTime = strftime("%H:%M:%S", localtime())
                print(f"# {outerIter}th run finished after {innerIter} iterations at {endTime}")

                return totalEdgeCost, steinerConnections

        maxNodeWeight = 0

    for edge in edgeList:
        totalEdgeCost += edge.cost
        if edge.start.connections > 3 or edge.end.connections > 3:
            steinerConnections = False

    endTime = strftime("%H:%M:%S", localtime())
    print(f"# {outerIter}th run finished after {innerIter} iterations at {endTime}")

    return totalEdgeCost, steinerConnections
