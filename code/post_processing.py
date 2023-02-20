# -*- coding: utf-8 -*-

"""
This file contains all post processing functions
@author: Jan Straub
"""

# Imports
from helper import calculate_distance_between_positions, find_other_edge_end, fermat_point


def remove_from_terminal(environmentNodeList,
                         environmentTerminalNodeList,
                         removeEdge):

    """_summary_
        Function removes all nodes between terminals and Steiner points that have two connections
    Args:
        environmentNodeList (list): List of node objects
        environmentTerminalNodeList (list): List of terminal node objects
        removeEdge (function): Class function to remove nodes

    Returns:
        newEdgeList (list): List of new edges that where created
    """

    newEdgeList = []

    for terminal in environmentTerminalNodeList:
        if len(terminal.nodeEdgeList) != 0:

            goingFurther = True
            start = current = terminal
            nextNode = None

            nodeListRemove = environmentNodeList.remove

            # Removed unused nodes and edges
            while goingFurther:

                for edge in reversed(current.nodeEdgeList):
                    nextNode = find_other_edge_end(current, edge)
                    nextSteinerPoint = nextNode.steinerPoint
                    currentTerminal = current.terminal
                    nextTerminal = nextNode.terminal

                    # No change needed
                    if currentTerminal and nextTerminal:
                        goingFurther = False

                    # Found terminal
                    elif not currentTerminal and nextTerminal:

                        removeEdge(edge)
                        del edge

                        if not currentTerminal:
                            nodeListRemove(current)

                        goingFurther = False

                        newEdgeList.append([start, nextNode])

                    # Next is Steiner point
                    elif nextSteinerPoint:

                        if not currentTerminal and current.connections < 2:
                            nodeListRemove(current)
                            removeEdge(edge)
                            del edge

                        goingFurther = False

                        if not currentTerminal or not nextSteinerPoint:
                            newEdgeList.append([start, nextNode])

                    # Next node in edge
                    elif not nextSteinerPoint:

                        removeEdge(edge)
                        del edge

                        if not currentTerminal:
                            nodeListRemove(current)

                        current = nextNode
                        goingFurther = True
                        break

                    else:
                        goingFurther = False

    return newEdgeList


def remove_from_steiner(environmentNodeList,
                        removeEdge, createSteinerEdge,
                        newEdgeList, steinerNodeList):

    """_summary_
        Function checks all edges between Steiner points for
        nodes with two connections
    Args:
        environmentNodeList (list): List of node objects
        removeEdge (function): Class function to remove nodes
        createSteinerEdge (function): Class function to create Steiner edges
        newEdgeList (list): List of new edges that where created
        steinerNodeList (list): List of all Steiner points
    """

    for steinerNode in steinerNodeList:
        if len(steinerNode.nodeEdgeList) != 0:

            goingFurther = True
            start = current = steinerNode
            nextNode = None

            nodeListRemove = environmentNodeList.remove

            # Removed unused nodes and edges
            while goingFurther:

                for edge in reversed(current.nodeEdgeList):
                    nextNode = find_other_edge_end(current, edge)
                    nextSteinerPoint = nextNode.steinerPoint
                    currentSteinerPoint = current.steinerPoint
                    nextTerminal = nextNode.terminal

                    # Next is Steiner point
                    if nextSteinerPoint or nextTerminal:

                        if not currentSteinerPoint:
                            nodeListRemove(current)
                            removeEdge(edge)
                            del edge
                            newEdgeList.append([start, nextNode])

                        goingFurther = False

                    # Next node in edge
                    elif not nextSteinerPoint:

                        removeEdge(edge)
                        del edge

                        if not currentSteinerPoint:
                            nodeListRemove(current)

                        current = nextNode
                        goingFurther = True
                        break

                    else:
                        goingFurther = False

    for newEdge in newEdgeList:
        createSteinerEdge(newEdge[0], newEdge[1])


def remove_rest_nodes(environmentNodeList, removeEdge,
                      createSteinerEdge, environmentEdgeList):

    """_summary_
        Function checks for nodes that still have two connections and
        removes them for a clear graph result
    Args:
        environmentNodeList (list): List of node objects
        removeEdge (function): Class function to remove nodes
        createSteinerEdge (function): Class function to create Steiner edges
        environmentEdgeList (list): List of edge objects
    """

    iterate = True

    while iterate:
        checkEdgeList, nodeCheckList = [], []
        for edge in environmentEdgeList:
            startNode, endNode = edge.start, edge.end
            if [startNode, endNode] not in checkEdgeList and [endNode, startNode] not in checkEdgeList:
                checkEdgeList.append([startNode, endNode])
            else:
                removeEdge(edge)
                del edge

        unusedNodeList = []
        for node in environmentNodeList:
            if node.connections == 2:
                unusedNodeList.append(node)
                nodeCheckList.append(False)
            else:
                nodeCheckList.append(True)

        for node in reversed(unusedNodeList):

            createSteinerEdge(node.neighbors[0], node.neighbors[1])

            for edge in reversed(node.nodeEdgeList):
                removeEdge(edge)

                del edge

            if not node.terminal:

                unusedNodeList.remove(node)
                environmentNodeList.remove(node)

                del node

        if all(nodeCheckList):
            iterate = False


def remove_unused_grid_nodes(environmentNodeList,
                             environmentTerminalNodeList,
                             removeEdge, createSteinerEdge,
                             environmentEdgeList):

    """_summary_
        Function starts three different cleaning functions to remove
        all unwanted nodes in the graph and designates all nodes with 3 connections as Steiner points
    Args:
        environmentNodeList (list): List of node objects
        environmentTerminalNodeList (list): List of terminal node objects
        removeEdge (function): Class function to remove nodes
        createSteinerEdge (function): Class function to create Steiner edges
        environmentEdgeList (list): List of edge objects
    """

    steinerNodeList = []

    for node in environmentNodeList:
        if node.connections == 3:
            node.steinerPoint = True
            steinerNodeList.append(node)

    newEdgeList = remove_from_terminal(environmentNodeList,
                                       environmentTerminalNodeList,
                                       removeEdge)

    remove_from_steiner(environmentNodeList, removeEdge,
                        createSteinerEdge, newEdgeList, steinerNodeList)

    # remove_rest_nodes(environmentNodeList, removeEdge, createSteinerEdge,
    # environmentEdgeList)


def fermat_torricelli_point_calculation(environmentNodeList):

    """_summary_
        Finds Fermat point (Steiner point) and iterates as long as the position of the point changes
    Args:
        environmentNodeList (list): List of node objects
    """

    iterate = True

    while iterate:

        oldNodeList, distanceList = [], []

        for node in environmentNodeList:
            oldNodeList.append(node.position)

            if node.connections == 3 and not node.terminal:

                A, B, C = [], [], []

                for pos, neighbor in enumerate(node.neighbors):
                    x, y = neighbor.position

                    if pos == 0:
                        A = [x, y]
                    if pos == 1:
                        B = [x, y]
                    if pos == 2:
                        C = [x, y]

                node.position = fermat_point(A, B, C)

        for pos, position in enumerate(oldNodeList):
            distance = calculate_distance_between_positions(
                position, environmentNodeList[pos].position)

            if distance > 0.1:
                distanceList.append(False)
            else:
                distanceList.append(True)

        if all(distanceList):
            iterate = False


def remove_nodes_within_radius(environmentNodeList, removeEdge,
                               createSteinerEdge):

    """_summary_
        Remove any Steiner point that is to close to a terminal
    Args:
        environmentNodeList (list): List of node objects
        environmentTerminalNodeList (list): List of terminal node objects
    """

    for node in reversed(environmentNodeList):
        if not node.terminal and node.steinerPoint:
            terminal = None
            for edge in reversed(node.nodeEdgeList):
                neighbor = find_other_edge_end(node, edge)
                if calculate_distance_between_positions(
                    node.position, neighbor.position) < 0.1 and neighbor.terminal is True:
                    terminal = neighbor
                    removeEdge(edge)
            if terminal is not None:
                for edge in reversed(node.nodeEdgeList):
                    if edge.start == node:
                        createSteinerEdge(terminal, edge.end)
                        removeEdge(edge)
                    else:
                        createSteinerEdge(edge.start, terminal)
                        removeEdge(edge)
                environmentNodeList.remove(node)
