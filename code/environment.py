# -*- coding: utf-8 -*-

"""
This file is used to create the network environment
@author: Jan Straub
"""

# Imports
from math import pi

from grid_components import EDGE
from create_grid import create_grid_nodes, create_grid_edges
from helper import calculate_distance_between_positions


class ENVIRONMENT:
    """_summary_
        Class is used to create the environment for the graph and the agents to operate upon
    """

    def __init__(self, jsonNodeList,
                 xMin, xMax, yMin, yMax, viscosity):

        """_summary_
            Create environment object
        Args:
            jsonNodeList (list): Json list of the original nodes
            xMin (float): Minimal x value of original nodes
            xMax (float): Maximum x value of original nodes
            yMin (float): Minimal y value of original nodes
            yMax (float): Maximum y value of original nodes
            viscosity (float): Viscosity of fluid.
        """

        self.environmentNodeList = []
        self.environmentTerminalNodeList = []
        self.environmentEdgeList = []

        self.create_grid_environment(jsonNodeList,
                                     xMin, xMax, yMin, yMax, viscosity)


    def create_grid_environment(self, jsonNodeList,
                                xMin, xMax, yMin, yMax, viscosity):

        """_summary_
            Function creates point grid
        Args:
            jsonNodeList (list): Json list of the original nodes
            xMin (float): Minimal x value of original nodes
            xMax (float): Maximum x value of original nodes
            yMin (float): Minimal y value of original nodes
            yMax (float): Maximum y value of original nodes
            viscosity (float): Viscosity of fluid.
        """

        create_grid_nodes(jsonNodeList,
                          xMin, xMax, yMin, yMax,
                          self.environmentNodeList,
                          self.environmentTerminalNodeList)

        create_grid_edges(yMin, yMax, viscosity,
                          self.environmentNodeList,
                          self.environmentEdgeList)

        self.set_node_and_edge_weight(jsonNodeList)


    def set_node_and_edge_weight(self, jsonNodeList):

        """_summary_
            Function sets node and edge weights
        Args:
            jsonNodeList (list): Json list of the original nodes
        """

        enviromentEdgeListLength = len(self.environmentEdgeList)

        for node in self.environmentNodeList:
            nodePosition = node.position

            for terminal in jsonNodeList:
                node.weight += calculate_distance_between_positions(nodePosition, terminal)

        for edge in self.environmentEdgeList:
            edge.cost = (edge.start.weight + edge.end.weight) / enviromentEdgeListLength


    def remove_edge(self, edge):

        """_summary_
            Function removes edge from nodeEdgeList and edgeList,
            removes one connections for edge start and end node and removes neighbours
        Args:
            edge (object): Edge object that is removed
        """

        edgeStartNode = edge.start
        edgeEndNode = edge.end

        edgeStartNode.nodeEdgeList.remove(edge)
        edgeEndNode.nodeEdgeList.remove(edge)

        edgeStartNode.connections -= 1
        edgeEndNode.connections -= 1

        edgeStartNode.neighbours.remove(edgeEndNode)
        edgeEndNode.neighbours.remove(edgeStartNode)

        self.environmentEdgeList.remove(edge)
        del edge


    def create_steiner_edge(self, startNode, nextNode):

        """_summary_
            Function creates steiner edge
        Args:
            startNode (object): Start node object of the steiner edge
            nextNode (object): End node object of the steiner edge
        """

        startId = startNode.nodeObjectId
        nextId = nextNode.nodeObjectId
        edgeId = ""
        piFactor = pi ** 4

        if startId < nextId:
            edgeId = str(startId) + "-" + str(nextId)
        else:
            edgeId = str(nextId) + "-" + str(startId)

        if edgeId not in self.environmentEdgeList:

            edge = EDGE(edgeId, nextNode, startNode, piFactor)

            # Add new edge
            startNode.nodeEdgeList.append(edge)
            nextNode.nodeEdgeList.append(edge)

            startNode.connections += 1
            nextNode.connections += 1

            startNode.neighbours.append(nextNode)
            nextNode.neighbours.append(startNode)

            self.environmentEdgeList.append(edge)
            edge.steinerEdge = True
