# -*- coding: utf-8 -*-

# Imports
import numpy as np

from matplotlib.collections import LineCollection


"""_summary_
Class used to create the environment for the graph and the agents to operate upon
Returns:
    _type_: _description_
    environment: Object which serves as a controller for the algorithm
"""
class Environment:
    
    def __init__(self):
        self._nodeList = []
        self._edgeList = []
                
                
    """_summary_
    Method uses to create node objects and save them in the nodes list for easy access
    """
    def createNodes(self, nodeList):
        for i in range(0, len(nodeList)):
            node = Node(i, nodeList[i])      
            self._nodeList.append(node)
        
        return
    
    
    #TODO create Steiner point function
         
    
    """_summary_
    Create the edges between the nodes as a way to allow agents to spawn on them
    """
    def createEdges(self, edgeList, edgeCost):  
        
        for i in range(0, len(self._nodeList)):
            for j in range(0, len(edgeList)):
                if self._nodeList[i]._id == edgeList[j][0]:
                    edge = Edge(j, self._nodeList[i], self._nodeList[edgeList[j][1]], edgeCost)
                    
                    self._nodeList[i]._nodeEdgeList.append(edge)
                    self._edgeList.append(edge)
                    self._nodeList[i]._connections += 1
                    
                    if (edge._start._id != self._nodeList[i]._id):
                        self._nodeList[i]._neighbourIDs.append(edge._start._id)
                    elif (edge._end._id != self._nodeList[i]._id):
                        self._nodeList[i]._neighbourIDs.append(edge._end._id)
                
        for i in range(0, len(self._nodeList)):
            for j in range(0, len(edgeList)):
                if self._nodeList[i]._id == edgeList[j][1]:
                    self._nodeList[i]._nodeEdgeList.append(self._edgeList[j])
                    self._nodeList[i]._connections += 1
                    
                    if (edge._start._id != self._nodeList[i]._id):
                        self._nodeList[i]._neighbourIDs.append(edge._start._id)
                    elif (edge._end._id != self._nodeList[i]._id):
                        self._nodeList[i]._neighbourIDs.append(edge._end._id)
    
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
        
        for edge in self._edgeList:
            edges.append([edge._start._id, edge._end._id])
            edgeWidth.append(edge._radius * 2)
        
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
        self._flux = 0
        self._initialPressure = 1
        self._connections = 0
        self._sink = False
        self._pressureVector = []
        self._nodeEdgeList = []    
        self._neighbourIDs = []
            
################################################################################

"""_summary_
Creates edge object
Returns:
    _type_: _description_
    edge: Graph edge
"""
class Edge:
    
    def __init__(self, id, start, end,  cost = 1, length = 1, radius = 1):
        self._id = id
        self._length = length 
        self._cost = cost #TODO figure out how to implement
        self._radius = radius
        self._start = start
        self._end = end
        self._conductivity = 0
        self._flux = 0