# -*- coding: utf-8 -*-

"""
This file contains the grid component objects (node, edge)
@author: Jan Straub
"""

class NODE:
    """_summary_
        Creates node object
    """

    def __init__(self, nodeId, position):

        """_summary_
            Creates node object
        Args:
            nodeId (int): Id of node object
            position (list): Position of object in space
        """

        self.nodeObjectId, self.position = nodeId, position
        self.pressure, self.connections, self.totalEdgeCost, self.weight, self.terminalNodeId = 0, 0, 0, 0, 0
        self.sink, self.terminal, self.steinerPoint = False, False, False
        self.nodeEdgeList, self.neighbours = [], []

################################################################################

class EDGE:
    """_summary_
        Creates edge object
    """

    def __init__(self, edgeId, start, end, piFactor,
                 length = 1, viscosity = 0.5):

        """_summary_
            Created edge object
        Args:
            edgeId (int): Id of edge object
            start (object): Start node of edge
            end (object): End node of edge
            piFactor (float): Constant
            length (int, optional): Length of edge. Defaults to 1.
            viscosity (float, optional): Viscosity of fluid. Defaults to 0.5.
        """

        self.edgeObjectId, self.start, self.end, self.length = edgeId, start, end, length
        self.cost, self.compositeCost, self.neighbourFactor, self.radius = 0, 1, 0, 1
        self.conductivity, self.edgeControlPointsList = [piFactor / (8 * viscosity)] * 2, []
        self.steinerEdge = False
