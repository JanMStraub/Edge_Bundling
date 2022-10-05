# -*- coding: utf-8 -*-

# Imports
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection

from helper import findNodeByPosition, calculateDistanceBetweenPositions


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
                            if (createdEdge._start == node and createdEdge._end == endNode) or (createdEdge._end == node and createdEdge._start == endNode):
                                newEdge = False 
                                existingEdge = createdEdge
                        
                        if (newEdge):
                            edge = Edge(id, node, endNode)
                            self._edgeList.append(edge)
                            node._nodeEdgeList.append(edge)
                            id += 1
                        else: 
                            node._nodeEdgeList.append( )
                               
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
                            if (createdEdge._start == node and createdEdge._end == endNode) or (createdEdge._end == node and createdEdge._start == endNode):
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
                            if (createdEdge._start == node and createdEdge._end == endNode) or (createdEdge._end == node and createdEdge._start == endNode):
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
                            if (createdEdge._start == node and createdEdge._end == endNode) or (createdEdge._end == node and createdEdge._start == endNode):
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

 
    def setNodeAndEdgeWeight(self, terminalNodeList):
        for node in self._nodeList:
            weight = 0
        
            for terminal in terminalNodeList:
                weight += calculateDistanceBetweenPositions(node._position, terminal)
            
            node._weight = weight / len(terminalNodeList)
            
        for edge in self._edgeList:
            edge._cost = (edge._start._weight + edge._end._weight) / len(self._edgeList)
        
        return
    
    
    """_summary_
    Function creates point grid
    """
    def createGrid(self, nodeList):
        xMin, xMax, yMin, yMax = self.createGridNodes(nodeList)
        self.createGridEdges(xMin, xMax, yMin, yMax)       
        self.createTerminalNodes(nodeList)
        self.setNodeAndEdgeWeight(nodeList)
        
        return

 
    """_summary_
    Plot edges and nodes in matplotlib
    """
    def plotGraph(self, t, tau):
        
        fig = plt.figure()
        fig = plt.figure(figsize = (10, 10))
        ax = fig.add_subplot(111)
        ax.set_title("Polycephalum Test - step: {} - tau: {}".format(t + 1, tau))
        
        G = nx.Graph()
        
        edgeLabels = dict()
        nodeLabels = dict()
        colorValues = list()
        edgeWidth = list()

        for node in self._nodeList:
            x, y, z = node._position
            G.add_node(node._id, pos = (x, y))
            nodeLabels[node._id] = round(node._weight, 2) # [round(a, 2) for a in node._pressureVector[:3]]
        
            if node in self._terminalNodeList:
                colorValues.append("red")
            else:
                colorValues.append("blue")
        
        for edge in self._edgeList:
            G.add_edge(edge._start._id, edge._end._id)
            edgeLabels[edge._start._id, edge._end._id] = round(edge._cost, 2) # round(edge._cost, 4) # round(edge._conductivity[1], 4)
            edgeWidth.append(edge._radius / (len(self._edgeList) * 100))    
        
        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, node_color = colorValues)
        nx.draw_networkx_labels(G, pos, nodeLabels)
        # nx.draw_networkx_nodes(G, pos, node_size=8, alpha=0.5)
        nx.draw_networkx_edge_labels(G, pos, edgeLabels)
        plt.tight_layout()
        
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
        self._initialPressure = 1
        self._connections = 0
        self._weight = 0
        self._totalEdgeCost = 0
        self._sink = False
        self._terminal = False
        self._pressureVector = []
        self._nodeEdgeList = []    
        self._neighbourIDs = []
        self._neighbours = []
            
################################################################################

"""_summary_
Creates edge object
Returns:
    _type_: _description_
    edge: Graph edge
"""
class Edge:
    
    def __init__(self, id, start, end):
        self._id = id
        self._length = 1 
        self._cost = 1
        self._compositeCost = 0
        self._radius = 1
        self._start = start
        self._end = end
        self._conductivity = [0] * 2
        self._flux = 0