# -*- coding: utf-8 -*-

# Imports
import numpy as np

from helper import calculateEdges


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
        self._trailMap = np.zeros(shape = (N, M)) # Continuum-based layer
        self._controlMap = np.zeros(shape = (N, M)) # Graph-based layer
        self._nodeList = []
        self._edgeList = []
                
                
    """_summary_
    Method uses to create node objects and save them in the nodes list for easy access
    """
    def createNodes(self, nodes):
        for i in range(0, len(nodes)):
            node = Node(i, nodes[i])      
                  
            self._nodeList.append(node)
        
        return
    
    
    #TODO create Steiner point function
            
            
    """_summary_
    This function is only for testing purposes
    """     
    def spawnOffLimitNode(self, position, strength = -1, radius = 5):
        n, m = position
        y, x = np.ogrid[-n : self._N - n, -m : self._M - m]
        mask = x ** 2 + y ** 2 <= radius ** 2
        
        self._controlMap[mask] = strength  

        return
            
    
    """_summary_
    Spawn the created nodes on the trail map as "food" for the agents
    """
    def spawnNodes(self, scale, radius = 3, strength = 2):
        for entry in self._nodeList:
            a, b, c = entry._position
            
            # For testing
            a *= scale
            b *= scale
            y, x = np.ogrid[-a : self._N - a, -b : self._M - b]
            mask = x ** 2 + y ** 2 <= radius ** 2
            
            self._trailMap[mask] = strength  
            
        return
         
    
    """_summary_
    Create the edges between the nodes as a way to allow agents to spawn on them
    """
    def createEdges(self, edges, edgeCost):  
        
        for i in range(0, len(self._nodeList)): # 5
            for j in range(0, len(edges)): # 10
                if self._nodeList[i]._id == edges[j][0]:
                    edge = Edge(j, calculateEdges(self._nodeList[i], self._nodeList[edges[j][1]]), self._nodeList[i], self._nodeList[edges[j][1]], edgeCost, 1)
                    
                    self._nodeList[i]._nodeEdgeList.append(edge)
                    self._edgeList.append(edge)
                    self._nodeList[i]._connections += 1
                
                #TODO index error with real graph
                if self._nodeList[i]._id == edges[j][1]:
                    # self._edgeList.append(edge)
                    self._nodeList[i]._nodeEdgeList.append(self._edgeList[j])
                    self._nodeList[i]._connections += 1
        
        return
        
        
    """_summary_
    Spawn agents on the line connection the nodes
    """
    def spawnEdges(self, scale, sensorAngle = np.pi / 4, rotationAngle = np.pi / 8, sensorOffset = 9):        
        for entry in self._edgeList:
            for point in entry.points:
                N = point[0] * scale
                M = point[1] * scale
                if (self._dataMap[N, M] == 0 and self._controlMap[N, M] >= 0): # Check if pixel empty and not in offlimit area
                    self._dataMap[N, M] = 1
        
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