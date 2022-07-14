# -*- coding: utf-8 -*-

# Imports
import numpy as np
from scipy.ndimage import gaussian_filter
import random

from agent import Agent
from helper import calculateEdges

class Environment:
    
    def __init__(self, N = 200, M = 200, populationPercentage = 0.15):
        self.N = N
        self.M = M
        self.dataMap = np.zeros(shape=(N, M)) # Agent-based layer
        self.trailMap = np.zeros(shape=(N, M)) # Continuum-based layer
        self.population = int(self.N * self.M * populationPercentage)
        self.agents = []
        self.nodes = []
        self.edges = []
        
        
    def spawnAgents(self, sensorAngle = np.pi / 4, rotationAngle = np.pi / 8, sensorOffset = 9):
        while (np.sum(self.dataMap) < self.population):
            randomN = np.random.randint(self.N)
            randomM = np.random.randint(self.M)
            
            if (self.dataMap[randomN, randomM] == 0): # Check if pixel empty
                agent = Agent((randomN, randomM), sensorAngle, rotationAngle, sensorOffset)
                self.agents.append(agent)
                self.dataMap[randomN, randomM] = 1
                
   
    def createNodes(self, nodes, strength = 3, radius = 3):
        for i in range(0, len(nodes)):
            node = Node(i, nodes[i], strength, radius)            
            self.nodes.append(node)
            
    
    def spawnNodes(self, scale):
        for entry in self.nodes:
            a, b, c = entry.position
            
            # For testing
            a *= scale
            b *= scale
            y, x = np.ogrid[-a : self.N - a, -b : self.M - b]
            mask = x ** 2 + y ** 2 <= entry.radius ** 2
            self.trailMap[mask] = entry.strength  
         
            
    def createEdges(self, edges, strength = 3):  
        
        for i in range(0, len(self.nodes)):
            for j in range(0, len(edges)):
                if self.nodes[i].id == edges[j][0]:
                    edge = Edge(i, calculateEdges(self.nodes[i], self.nodes[edges[j][1]]), strength)
                    self.nodes[i].edges.append(edge)
                    self.edges.append(edge)
                    self.nodes[i].connections += 1
        
        
    def spawnEdges(self, sensorAngle = np.pi / 4, rotationAngle = np.pi / 8, sensorOffset = 9):        
        for entry in self.edges:
            for point in entry.points:
                N = point[0] * 3
                M = point[1] * 3
                if (self.dataMap[N, M] == 0): # Check if pixel empty
                    agent = Agent((N, M), sensorAngle, rotationAngle, sensorOffset)
                    self.agents.append(agent)
                    self.dataMap[N, M] = 1
        
        
    def diffusionOperator(self, decayRate = 0.6, sigma = 2):
        self.trailMap = decayRate * gaussian_filter(self.trailMap, sigma)
    
    
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
                randomSampleOrder[i].depositPhermoneTrail(self.trailMap)
    
    
    # Look for trails
    def sensoryStage(self):
        randomSampleOrder = random.sample(self.agents, len(self.agents))
        
        for i in range(len(randomSampleOrder)):
            randomSampleOrder[i].sense(self.trailMap)
            
################################################################################

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

class Edge:
    
    def __init__(self, id, points, strength):
        self.id = id
        self.points = points
        self.strength = strength
        