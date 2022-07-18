# -*- coding: utf-8 -*-

# Imports
import numpy as np
from scipy.ndimage import gaussian_filter
import random

from agent import Agent
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
        self.N = N
        self.M = M
        self.dataMap = np.zeros(shape=(N, M)) # Agent-based layer
        self.trailMap = np.zeros(shape=(N, M)) # Continuum-based layer
        self.controlMap = np.zeros(shape=(N, M)) # Graph-based layer
        self.agents = []
        self.nodes = []
        self.edges = []
                
                
    """_summary_
    Method uses to create node objects and save them in the nodes list for easy access
    """
    def createNodes(self, nodes, strength = 3, radius = 3):
        for i in range(0, len(nodes)):
            node = Node(i, nodes[i], strength, radius)            
            self.nodes.append(node)
            
    """_summary_
    This function is only for testing purposes
    """     
    def spawnOffLimitNode(self, position, strength = -1, radius = 5):
        n, m = position
        y, x = np.ogrid[-n : self.N - n, -m : self.M - m]
        mask = x ** 2 + y ** 2 <= radius ** 2
        self.controlMap[mask] = strength  
            
    
    """_summary_
    Spawn the created nodes on the trail map as "food" for the agents
    """
    def spawnNodes(self, scale):
        for entry in self.nodes:
            a, b, c = entry.position
            
            # For testing
            a *= scale
            b *= scale
            y, x = np.ogrid[-a : self.N - a, -b : self.M - b]
            mask = x ** 2 + y ** 2 <= entry.radius ** 2
            self.trailMap[mask] = entry.strength  
         
    
    """_summary_
    Create the edges between the nodes as a way to allow agents to spawn on them
    """
    def createEdges(self, edges, strength = 3):  
        for i in range(0, len(self.nodes)):
            for j in range(0, len(edges)):
                if self.nodes[i].id == edges[j][0]:
                    edge = Edge(i, calculateEdges(self.nodes[i], self.nodes[edges[j][1]]), strength)
                    self.nodes[i].edges.append(edge)
                    self.edges.append(edge)
                    self.nodes[i].connections += 1
        
    
    """_summary_
    Spawn agents on the line connection the nodes
    """
    def spawnEdges(self, scale, sensorAngle = np.pi / 4, rotationAngle = np.pi / 8, sensorOffset = 9):        
        for entry in self.edges:
            for point in entry.points:
                N = point[0] * scale
                M = point[1] * scale
                if (self.dataMap[N, M] == 0 and self.controlMap[N, M] >= 0): # Check if pixel empty
                    agent = Agent((N, M), sensorAngle, rotationAngle, sensorOffset)
                    self.agents.append(agent)
                    self.dataMap[N, M] = 1
        
    
    """_summary_
    Used to diffuse the values on the trailMap to mimic natural diffusion of pheromones
    """
    def diffusionOperator(self, decayRate = 0.6, sigma = 2):
        
        #TODO exception for nodes
        
        self.trailMap = decayRate * gaussian_filter(self.trailMap, sigma)
    
    
    """_summary_
    Check if the destination of the agent is occupied
    """
    def checkSurroundings(self, pixel, angle):
        n, m = pixel
        
        # Check directions
        x = np.cos(angle)
        y = np.sin(angle)
        
        # Pixel unoccupied
        if (self.dataMap[(n - round(x)) % self.N, (m + round(y)) 
                         % self.M] == 0):
            return ((n - round(x)) % self.N, (m + round(y)) % self.M)
        # Pixel occupied
        elif (self.dataMap[(n - round(x)) % self.N, (m + round(y)) 
                           % self.M] == 1):
            return pixel
       
    
    """_summary_
    Move the agent to the new position if the dataMap allows it
    """
    def motorStage(self):
        randomSampleOrder = random.sample(self.agents, len(self.agents))
        
        for i in range(len(randomSampleOrder)):
            oldX, oldY = randomSampleOrder[i].position
            newX, newY = self.checkSurroundings(randomSampleOrder[i].position, randomSampleOrder[i].phi)
            
            if ((newX,newY) == (oldX, oldY)):
                randomSampleOrder[i].phi = 2 * np.pi * np.random.random()
                randomSampleOrder[i].updateSensors()
            else:
                randomSampleOrder[i].position = (newX, newY)
                randomSampleOrder[i].updateSensors()
                self.dataMap[oldX,oldY] = 0
                self.dataMap[newX,newY] = 1
                randomSampleOrder[i].depositPheromoneTrail(self.trailMap)
    

    """_summary_
    Look for trails in the trailMap by using the sense() function of each agent
    """
    def sensoryStage(self):
        randomSampleOrder = random.sample(self.agents, len(self.agents))
        
        for i in range(len(randomSampleOrder)):
            randomSampleOrder[i].sense(self.trailMap, self.controlMap)
            
################################################################################

"""_summary_
Creates node object
Returns:
    _type_: _description_
    node: Graph node
"""
class Node:
    
    def __init__(self, id, position, strength, radius):
        self.id = id
        self.position = position
        self.strength = strength
        self.radius = radius
        self.connections = 0
        self.neighbours = []
        self.edges = []
        
            
################################################################################

"""_summary_
Creates edge object
Returns:
    _type_: _description_
    edge: Graph edge
"""
class Edge:
    
    def __init__(self, id, points, strength):
        self.id = id
        self.points = points
        self.strength = strength
        
################################################################################