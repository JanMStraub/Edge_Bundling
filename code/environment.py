# -*- coding: utf-8 -*-

# Imports
import scipy.misc

import numpy as np

from skimage.draw import line

from helper import calculateEdgePoints


"""_summary_
Class used to create the environment for the graph and the agents to operate upon
Returns:
    _type_: _description_
    environment: Object which serves as a controller for the algorithm
    dataMap: Agent-based layer
    trailMap: Continuum-based layer (Nodes)
    controlMap: Map for managing the off limit areas for agents
"""
class Environment:
    
    def __init__(self, N = 200, M = 200):
        self._N = N
        self._M = M
        self._dataMap = np.zeros(shape = (N, M)) # Agent-based layer
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
    Spawn the created nodes on the trail map as "food" for the agents
    """
    def spawnNodes(self, scale, radius = 3):
        for entry in self._nodeList:
            a, b, c = entry._position
          
            a *= scale
            b *= scale
            y, x = np.ogrid[-a : self._N - a, -b : self._M - b]
            mask = x ** 2 + y ** 2 <= radius ** 2
            
            self._dataMap[mask] = 1  
            
        return
         
    
    """_summary_
    Create the edges between the nodes as a way to allow agents to spawn on them
    """
    def createEdges(self, edgeList, edgeCost):  
        
        for i in range(0, len(self._nodeList)):
            for j in range(0, len(edgeList)):
                if self._nodeList[i]._id == edgeList[j][0]:
                    edge = Edge(j, calculateEdgePoints(self._nodeList[i], self._nodeList[edgeList[j][1]]), self._nodeList[i], self._nodeList[edgeList[j][1]], edgeCost, 1)
                    
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
    Spawn agents on the line connection the nodes
    """
    def spawnEdges(self, scale):        
        
        for entry in self._edgeList:    
            rr, cc = line(entry._start._position[0] * scale, entry._start._position[1] * scale, entry._end._position[0] * scale, entry._end._position[1] * scale)
            self._dataMap[rr, cc] = 1

        return
            
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
        self._pressureVector = []
        self._connections = 0
        self._sink = False
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
    
    def __init__(self, id, points, start, end,  cost = 1, length = 1, radius = 1):
        self._id = id
        self._points = points
        self._length = length 
        self._cost = cost #TODO figure out how to implement
        self._radius = radius
        self._start = start
        self._end = end
        self._conductivity = 0
        self._flux = 0