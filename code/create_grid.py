# -*- coding: utf-8 -*-

"""
This file contains everyting to create a graph-grid
@author: Jan Straub
"""

# Imports
from math import pi

from grid_components import NODE, EDGE


def create_grid_nodes(jsonNodeList,
                      xMin, xMax, yMin, yMax,
                      environmentNodeList,
                      environmentTerminalNodeList):

    """_summary_
        Function is used to create node grid
    Args:
        jsonNodeList (list): Json list of the original nodes
        xMin (float): Minimal x value of original nodes
        xMax (float): Maximum x value of original nodes
        yMin (float): Minimal y value of original nodes
        yMax (float): Maximum y value of original nodes
    """

    nodeId = 0
    jsonList = []

    environmentNodeListAppend = environmentNodeList.append
    enviromentTerminalNodeListAppend = environmentTerminalNodeList.append

    for position in jsonNodeList:
        jsonList.append(list(position))

    for x in range(int(xMin), int(xMax) + 1):
        for y in range(int(yMin), int(yMax) + 1):
            node = NODE(nodeId, [float(x), float(y)])

            if [float(x), float(y)] in jsonList:
                node.terminal = True
                node.terminalNodeId = jsonList.index([float(x), float(y)])
                enviromentTerminalNodeListAppend(node)

            environmentNodeListAppend(node)
            nodeId += 1


def create_grid_edges(yMin, yMax, viscosity,
                      enviromentNodeList,
                      environmentEdgeList):

    """_summary_
        Function creates edges between nodes
    Args:
        yMin (float): Minimum y value of original nodes
        yMax (float): Maximum y value of original nodes
        viscosity (float): Viscosity of fluid.
    """

    edgeIds = {}
    numberOfNodes = len(enviromentNodeList)
    piFactor = pi ** 4
    yLength = int(yMax - yMin + 1)

    for index, node in enumerate(enviromentNodeList):
        # left down corner
        if index == 0:
            # up
            create_edge(node, enviromentNodeList[index + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # right
            create_edge(node, enviromentNodeList[index + yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal
            create_edge(node, enviromentNodeList[index + yLength + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)

        # left upper corner
        elif index == yLength - 1:
            # down
            create_edge(node, enviromentNodeList[index - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # right
            create_edge(node, enviromentNodeList[index + yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal
            create_edge(node, enviromentNodeList[index + yLength - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)

        # right down corner
        elif index == numberOfNodes - yLength:
            # up
            create_edge(node, enviromentNodeList[index + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # left
            create_edge(node, enviromentNodeList[index - yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal
            create_edge(node, enviromentNodeList[index - yLength + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)

        # right upper corner
        elif index == numberOfNodes - 1:
            # down
            create_edge(node, enviromentNodeList[index - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # left
            create_edge(node, enviromentNodeList[index - yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal
            create_edge(node, enviromentNodeList[index - yLength - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)

        # between left down corner and left upper corner
        elif 0 < index < yLength:
            # down
            create_edge(node, enviromentNodeList[index - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # up
            create_edge(node, enviromentNodeList[index + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # right
            create_edge(node, enviromentNodeList[index + yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal down
            create_edge(node, enviromentNodeList[index + yLength - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal up
            create_edge(node, enviromentNodeList[index + yLength + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)

        # between right down corner and right upper corner
        elif numberOfNodes - yLength < index < numberOfNodes - 1:
            # down
            create_edge(node, enviromentNodeList[index - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # up
            create_edge(node, enviromentNodeList[index + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # left
            create_edge(node, enviromentNodeList[index - yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal down
            create_edge(node, enviromentNodeList[index - yLength - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal up
            create_edge(node, enviromentNodeList[index - yLength + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)

        # between left down corner and right down corner
        elif index > 0 and index != numberOfNodes - yLength and index % yLength == 0:
            # up
            create_edge(node, enviromentNodeList[index + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # left
            create_edge(node, enviromentNodeList[index - yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # right
            create_edge(node, enviromentNodeList[index + yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal left
            create_edge(node, enviromentNodeList[index - yLength + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal right
            create_edge(node, enviromentNodeList[index + yLength + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)

        # between left upper corner and right upper corner
        elif index != yLength - 1 and index != numberOfNodes - 1 and index % yLength == yLength - 1:
            # down
            create_edge(node, enviromentNodeList[index - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # left
            create_edge(node, enviromentNodeList[index - yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # right
            create_edge(node, enviromentNodeList[index + yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal left
            create_edge(node, enviromentNodeList[index - yLength - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal right
            create_edge(node, enviromentNodeList[index + yLength - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)

        # all nodes in the midle
        else:
            # up
            create_edge(node, enviromentNodeList[index + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # down
            create_edge(node, enviromentNodeList[index - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # left
            create_edge(node, enviromentNodeList[index - yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # right
            create_edge(node, enviromentNodeList[index + yLength],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal down left
            create_edge(node, enviromentNodeList[index - yLength - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal down right
            create_edge(node, enviromentNodeList[index + yLength - 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal up left
            create_edge(node, enviromentNodeList[index - yLength + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)
            # diagonal up right
            create_edge(node, enviromentNodeList[index + yLength + 1],
                        edgeIds, viscosity, piFactor,
                        environmentEdgeList)


def create_edge(node, endNode, edgeIds,
                viscosity, piFactor,
                environmentEdgeList):

    """_summary_
        Creates edge between node and endNode,
        adds connection to each node,
        adds node to neighbour list and adds edge to edgeList and to each nodeEdgeList
    Args:
        node (object): Node object from which the edge begins
        endNode (object): Node object that is at the end of the edge
        edgeIds (list): List of all edge Ids
        viscosity (float): Viscosity of the fluid
        piFactor (float): Constant
    """

    edgeId = ""
    nodeEdgeListAppend = node.nodeEdgeList.append

    if node.nodeObjectId < endNode.nodeObjectId:
        edgeId = str(node.nodeObjectId) + "-" + str(endNode.nodeObjectId)
    else:
        edgeId = str(endNode.nodeObjectId) + "-" + str(node.nodeObjectId)

    if edgeId not in edgeIds:
        edge = EDGE(edgeId, node, endNode, viscosity, piFactor)

        environmentEdgeList.append(edge)
        nodeEdgeListAppend(edge)
        edgeIds[edgeId] = edge
    else:
        nodeEdgeListAppend(edgeIds.get(edgeId))

    node.connections += 1
    node.neighbours.append(endNode)
