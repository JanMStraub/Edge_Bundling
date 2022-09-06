# -*- coding: utf-8 -*-

# Imports
import heapq

import numpy as np

from matplotlib.collections import LineCollection

from helper import findNodeByPosition

from helper import findNodeById, calculateDistance


"""_summary_
Class used to create the environment for the graph and the agents to operate upon
Returns:
    _type_: _description_
    environment: Object which serves as a controller for the algorithm
"""
class Environment:
    
    def __init__(self):
        self._nodeList = []
        self._terminalNodeList = []
        self._edgeList = []
        self._terminalEdgeList = []
    
    
    """_summary_
    Function is used to create node grid
    """
    def createGridNodes(self, nodeList):
        id = 0
        xMin, xMax, yMin, yMax = float("inf"), 0.0, float("inf"), 0.0
        
        for node in nodeList:
            x, y, z = node
            
            if (x < xMin):
                xMin = x
            
            if (x > xMax):
                xMax = x

            if (y < yMin):
                yMin = y

            if (y > yMax):
                yMax = y
        
        print("xMin: {}, xMax: {}, yMin: {}, yMax: {}".format(xMin, xMax, yMin, yMax))
        
        for x in range(int(xMin), int(xMax) + 1):
            for y in range(int(yMin), int(yMax) + 1):
                node = Node(id, [float(x), float(y), z])
                self._nodeList.append(node)
                id += 1
        
        return xMin, xMax, yMin, yMax
    
    
    def createGridEdges(self, xMin, xMax, yMin, yMax):
        id = 0
        
        for node in self._nodeList:
            x, y, z = node._position
            
            for i in range(0, 4): 
                if i == 0:
                    if x != xMax:
                        existingEdge = None
                        newEdge = True
                        value = x + 1.0
                        endNode = findNodeByPosition(self._nodeList, value, y, z)
                        for createdEdge in self._edgeList:
                            if createdEdge._start == endNode:
                                newEdge = False 
                                existingEdge = createdEdge
                        
                        if (newEdge):
                            edge = Edge(id, node, endNode)
                            self._edgeList.append(edge)
                            node._nodeEdgeList.append(edge)
                            id += 1
                        else: 
                            node._nodeEdgeList.append(existingEdge)
                               
                        node._connections += 1
                        node._neighbours.append(endNode)
                        node._neighbourIDs.append(endNode._id)
                                
                if i == 1:
                    if y != yMax:
                        existingEdge = None
                        newEdge = True
                        value = y + 1.0
                        endNode = findNodeByPosition(self._nodeList, x, value, z)
                        for createdEdge in self._edgeList:
                            if createdEdge._start == endNode:
                                newEdge = False 
                                existingEdge = createdEdge
                        
                        if (newEdge):
                            edge = Edge(id, node, endNode)
                            self._edgeList.append(edge)
                            node._nodeEdgeList.append(edge)
                            id += 1
                        else: 
                            node._nodeEdgeList.append(existingEdge)
                               
                        node._connections += 1
                        node._neighbours.append(endNode)
                        node._neighbourIDs.append(endNode._id)
                    
                if i == 2:
                    if x != xMin:
                        existingEdge = None
                        newEdge = True
                        value = x - 1.0
                        endNode = findNodeByPosition(self._nodeList, value, y, z)
                        for createdEdge in self._edgeList:
                            if createdEdge._start == endNode:
                                newEdge = False 
                                existingEdge = createdEdge
                        
                        if (newEdge):
                            edge = Edge(id, node, endNode)
                            self._edgeList.append(edge)
                            node._nodeEdgeList.append(edge)
                            id += 1
                        else: 
                            node._nodeEdgeList.append(existingEdge)
                               
                        node._connections += 1
                        node._neighbours.append(endNode)
                        node._neighbourIDs.append(endNode._id)
                    
                if i == 3:
                    if y != yMin:
                        existingEdge = None
                        newEdge = True
                        value = y - 1.0
                        endNode = findNodeByPosition(self._nodeList, x, value, z)
                        for createdEdge in self._edgeList:
                            if createdEdge._start == endNode:
                                newEdge = False 
                                existingEdge = createdEdge
                        
                        if (newEdge):
                            edge = Edge(id, node, endNode)
                            self._edgeList.append(edge)
                            node._nodeEdgeList.append(edge)
                            id += 1
                        else: 
                            node._nodeEdgeList.append(existingEdge)
                               
                        node._connections += 1
                        node._neighbours.append(endNode)
                        node._neighbourIDs.append(endNode._id)
                
        return
        
    
    """_summary_
    Function creates point grid
    """
    def createGrid(self, nodeList):
        xMin, xMax, yMin, yMax = self.createGridNodes(nodeList)
        self.createGridEdges(xMin, xMax, yMin, yMax)       

        return
        
                
    """_summary_
    Method uses to create node objects and save them in the nodes list for easy access
    """
    def createTerminalNodes(self, nodeList):
        id = 0
        for node in nodeList:
            x, y, z = node
            selectedNode = findNodeByPosition(self._nodeList, x, y, z)
            selectedNode._terminal = True
            selectedNode._terminalId = id
            self._terminalNodeList.append(selectedNode)
            id += 1
        
        return
    
    
    """_summary_
    Use A* to create terminal edges in point-grid
    """
    def createTerminalEdges(self, edgeList):
        
        terminalId = 0
        id = self._edgeList[-1]._id
        
        for edge in edgeList:

            notFinished = True
            startNode = None
            endNode = None
            currentNode = None
            openList = []
            closedList = []
            
            for node in self._terminalNodeList:
                if edge[0] == node._terminalId:
                    startNode = node
                    
                if edge[1] == node._terminalId:
                    endNode = node
            
            for node in self._nodeList:
                node._parent = None
                            
            openList.append(startNode)
            
            while (len(openList) > 0 and notFinished):
                
                print(len(openList))

                currentNode = openList[0]
                currentIndex = 0
                
                for index, item in enumerate(openList):
                    if item._GHF[2] < currentNode._GHF[2]:
                        currentNode = item
                        currentIndex = index
                
                openList.pop(currentIndex)
                closedList.append(currentNode)
                
                if currentNode == endNode:
                    print("found")
                    path = []
                    current = currentNode
                    while current is not None:
                        path.append(current)
                        current = current._parent
                        
                    edge = Edge(id, startNode, endNode)
                    edge._routingNodes = path[::-1]
                    edge._terminalId = terminalId
                    self._terminalEdgeList.append(edge)
                    terminalId += 1
                    id += 1
                    notFinished = False
                
                for neighbour in currentNode._neighbours:
                    
                    if neighbour != startNode:
                        neighbour._parent = currentNode
                    
                    for closedNeighbour in closedList:
                        if neighbour == closedNeighbour:
                            break
                        
                    G = calculateEdgeLength(neighbour, startNode)
                    H = calculateEdgeLength(neighbour, endNode)
                    F = G + H
                    
                    neighbour._GHF = [G, H, F]
                    
                    for openNode in openList:
                        if neighbour == openNode and neighbour._GHF[0] > openNode._GHF[0]:
                            break
                    
                    openList.append(neighbour)

        return
   
    
    """_summary_
    Plot edges and nodes in matplotlib
    """
    def plotGraph(self, plt):
        nodes = list()
        edges = list()
        edgeWidth = list()
        
        for node in self._nodeList:
            a, b, c = node._position
            nodes.append([a, b])
    
        nodes = np.array(nodes)

        for edge in self._terminalEdgeList:
            for i in range(len(edge._routingNodes) - 1):
                edges.append([edge._routingNodes[i]._id, edge._routingNodes[i + 1]._id])
                edgeWidth.append(edge._radius)
        
        edges = np.array(edges)
        
        lc = LineCollection(nodes[edges], edgeWidth)
        plt.gca().add_collection(lc)
        plt.plot(nodes[:,0], nodes[:,1], 'ro')
        
        return plt
            
################################################################################

"""_summary_
Creates node object
Returns:
    _type_: _description_
    node: Graph node
"""
class Node:
    
    def __init__(self, id, position):
        self._id = id
        self._position = position
        self._terminalId = None
        self._parent = None
        self._initialPressure = 1
        self._connections = 0
        self._sink = False
        self._terminal = False
        self._pressureVector = []
        self._nodeEdgeList = []    
        self._neighbourIDs = []
        self._neighbours = []
        self._GHF = [0, 0, 0]
            
################################################################################

"""_summary_
Creates edge object
Returns:
    _type_: _description_
    edge: Graph edge
"""
class Edge:
    
    def __init__(self, id, start, end, cost = 1, length = 1, radius = 1):
        self._id = id
        self._terminalId = None
        self._length = length 
        self._cost = cost #TODO figure out how to implement
        self._radius = radius
        self._start = start
        self._end = end
        self._conductivity = 0
        self._terminal = False
        self._routingNodes = []