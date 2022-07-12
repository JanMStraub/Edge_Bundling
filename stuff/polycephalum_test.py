# -*- coding: utf-8 -*-

"""
PolyCenterephalum simulation
Based on the work of:
* Jeff Jones, UWE https://uwe-repository.worktribe.com/output/980579
* Sage Jensen https://sagejenson.com/physarum
* E. Carlbaum https://github.com/ecbaum/physarum/tree/8280cd131b68ed8dff2f0af58ca5685989b8cce7
* Amitav Mitra https://github.com/ammitra/Physarum
@author: Jan Straub
"""

# Imports
import numpy as np
from scipy.ndimage import gaussian_filter
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json


class Environment:
    
    def __init__(self, N = 200, M = 200, populationPercentage = 0.15):
        self.N = N
        self.M = M
        self.dataMap = np.zeros(shape=(N, M)) # Agent-based layer
        self.trailMap = np.zeros(shape=(N, M)) # Continuum-based layer
        self.population = int(self.N * self.M * populationPercentage)
        self.agents = []
        self.nodes = []
        
        
    def spawnAgents(self, sensorAngle = np.pi / 4, rotationAngle = np.pi / 8, sensorOffset = 9):
        while (np.sum(self.dataMap) < self.population):
            randomN = np.random.randint(self.N)
            randomM = np.random.randint(self.M)
            
            if (self.dataMap[randomN, randomM] == 0): # Check if pixel empty
                agent = Agent((randomN, randomM), sensorAngle, rotationAngle, sensorOffset)
                self.agents.append(agent)
                self.dataMap[randomN, randomM] = 1
                
   
    def spawnNodes(self, id, position, strength = 3, radius = 3):
        node = Node(id, position, strength, radius)
        self.nodes.append(node)
        
        n, m = position
        y, x = np.ogrid[-n : self.N - n, -m : self.M - m]
        mask = x ** 2 + y ** 2 <= radius ** 2
        self.trailMap[mask] = strength  
        
    
    def spawnEdges(self, position, strength = 1, radius = 1):
        n, m = position
        y, x = np.ogrid[-n : self.N - n, -m : self.M - m]
        mask = x ** 2 + y ** 2 <= radius ** 2
        self.trailMap[mask] = strength 
        
        
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
            
class Agent:
    
    def __init__(self, position, sensorAngle = np.pi / 8, rotationAngle = np.pi / 4, sensorOffset = 3):
        self.position = position
        self.phi = 2 * np.pi * np.random.random() # Looking direction
        self.sensorAngle = sensorAngle
        self.rotationAngle = rotationAngle
        self.sensorOffset = sensorOffset
        
        # Sensor initialization
        self.left = self.phi - sensorAngle
        self.center = self.phi
        self.right = self.phi + sensorAngle
        
        
    def depositPhermoneTrail(self, arr, strength = 1):
        n, m = self.position
        arr[n, m] = strength
        

    # Update sensor to new position
    def updateSensors(self):
        self.left = self.phi - self.sensorAngle
        self.center = self.phi              
        self.right = self.phi + self.sensorAngle
        
          
    def getSensorValues(self, arr):
        n, m = self.position
        row, column = arr.shape

        xLeft = round(self.sensorOffset*np.cos(self.left))
        yLeft = round(self.sensorOffset*np.sin(self.left))
        
        xCenter = round(self.sensorOffset*np.cos(self.center))
        yCenter = round(self.sensorOffset*np.sin(self.center))
        
        xRight = round(self.sensorOffset*np.cos(self.right))
        yRight = round(self.sensorOffset*np.sin(self.right))
        
        valueLeft = arr[(n - xLeft) % row, (m + yLeft) % column] 
        valueCenter = arr[(n - xCenter) % row, (m + yCenter) % column]
        valueRight = arr[(n - xRight) % row, (m + yRight) % column]  

        return (valueLeft, valueCenter, valueRight)
    

    def sense(self, arr):
        left, center, right = self.getSensorValues(arr)

        if ((center > left) and (center > right)):
            self.phi += 0
            self.updateSensors()
        elif ((left == right) and center < left):
            randomNumber = np.random.randint(2)
            if randomNumber == 0:
                self.phi += self.rotationAngle
                self.updateSensors()
            else:
                self.phi -= self.rotationAngle
                self.updateSensors()
        elif (right > left):
            self.phi += self.rotationAngle
            self.updateSensors()
        elif (left > right):
            self.phi -= self.rotationAngle
            self.updateSensors()
        else:
            self.phi += 0
            self.updateSensors()
            
################################################################################

class Node:
    
    def __init__(self, id, position, strength, radius):
        self.id = id
        self.position = position
        self.strength = strength
        self.radius = radius
        self.connections = 0
        self.neighbours = []
        
            
################################################################################

def readGraphData(path):
    
    # read graph data from JSON
    file = open(path)
    data = json.load(file)
    file.close()
    
    # Read relevant data
    numberOfNodes = data["graph"]["nodesNumber"]
    numberOfEdges = data["graph"]["edgesNumber"]
    edges = data["graph"]["edges"]
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
      
    return edges, nodes, numberOfEdges, numberOfNodes


def main():
    jsonFile = "code/data/simple_graph.json"
    N = 200
    M = 200
    populationPercentage = 0.15
    sensorAngle = np.pi / 8
    rotationAngle = np.pi / 4
    sensorOffset = 9
    decayRate = 0.85
    sigma = 0.65
    steps = 1
    intervals = 8
    
    ### Change to False if you want a gif ###
    plot = True
    
    edges, nodes, numberOfEdges, numberOfNodes = readGraphData(jsonFile)
    
    # Convert node to tupel
    for i in range(0, len(nodes)):
        node = Node(i, tuple(map(int, nodes["0"].strip("()").split(','))), 3, 3)
    
    environment = Environment(N, M, populationPercentage)
    environment.spawnAgents(sensorAngle, rotationAngle, sensorOffset)
    #environment.spawnNodes()
    
    if (plot):
        dt = int(steps / intervals)
        samples = np.linspace(0, dt * intervals, intervals + 1)
        
        for i in range(steps):
            environment.diffusionOperator(decayRate, sigma)   
            # environment.spawnNodes(nodes[])    
            
            environment.motorStage()
            environment.sensoryStage()
            print("Iteration: {}".format(i))
            
            if i == steps - 1:
                fig = plt.figure(figsize = (8, 8), dpi = 200)
                ax = fig.add_subplot(111)
                ax.imshow(environment.trailMap)
                ax.set_title("Polycephalum Test, step = {}".format(i + 1))
                ax.text(0, -10, "Sensor Angle: {:.2f} Sensor Offset: {} Rotation Angle: {:.2f} Population: {:.0f}%".format(np.degrees(sensorAngle), sensorOffset, np.degrees(rotationAngle), populationPercentage * 100))
                plt.savefig("simulation_t{}.png".format(i))
                plt.clf()
    else:
        ims = []
        fig = plt.figure(figsize = (8, 8), dpi = 100)
        ax = fig.add_subplot(111)
        
        for i in range(steps):
            environment.diffusionOperator(decayRate, sigma)
            
            environment.motorStage()
            environment.sensoryStage()
            print("Iteration: {}".format(i))
            
            txt = plt.text(0, -10, "iteration: {} Sensor Angle: {:.2f} Sensor Offset: {} Rotation Angle: {:.2f} Population: {:.0f}%".format(i, np.degrees(sensorAngle), sensorOffset, np.degrees(rotationAngle), populationPercentage * 100))
            im = plt.imshow(environment.trailMap, animated = True)
            ims.append([im, txt])
        
        fig.suptitle("Polycephalum Test")
        ani = animation.ArtistAnimation(fig, ims, interval = 50, blit = True, repeat_delay = 1000)
        ani.save("simulation.gif")
            
    return
    
if __name__ == "__main__":
    
    main()