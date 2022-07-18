# -*- coding: utf-8 -*-

# Imports
import numpy as np

"""_summary_
Class used to create agent object that deposits pheromone trail and can sense other pheromone trails left behind by other agents
Returns:
    _type_: _description_
    agent: Agent object with sensor functionality
"""
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
        
    
    """_summary_
    Function used to create pheromone trail after each iteration
    """
    def depositPheromoneTrail(self, arr, strength = 1):
        n, m = self.position
        arr[n, m] = strength
        

    """_summary_
    Update sensor to new position
    """
    def updateSensors(self):
        self.left = self.phi - self.sensorAngle
        self.center = self.phi              
        self.right = self.phi + self.sensorAngle
        

    """_summary_
    Checks pheromone values in front, to the left and to the right of the agent
    """
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
    

    """_summary_
    Uses values obtained by the getSensorValues() function to decide the direction for the next step
    """
    def sense(self, trailMap, controlMap):
        leftT, centerT, rightT = self.getSensorValues(trailMap)
        leftC, centerC, rightC = self.getSensorValues(controlMap)
        
        #TODO check if controlMap has negativ value
        #TODO what happens if agents spawn inside forbidden area
        
        if ((leftC < 0) and (centerC < 0) and (rightC < 0)): # facing restricted zone
            print("turn around")
            self.phi += np.pi # 180 degree turn
            self.updateSensors()
        elif ((leftC < 0) and (centerC < 0) and (rightC >= 0)): # left blocked
            print("avoid left")
            self.phi += self.rotationAngle
            self.updateSensors()
        elif ((leftC >= 0) and (centerC < 0) and (rightC < 0)): # right blocked
            print("avoid right")
            self.phi -= self.rotationAngle
            self.updateSensors()
        elif ((leftC < 0) and (centerC >= 0) and (rightC < 0)): # left and right blocked
            print("walk through")
            self.phi += 0
            self.updateSensors()
        elif ((centerC < 0) and ((leftC >= 0) or (rightC >= 0))): # center blocked
            print("left or right")
            randomNumber = np.random.randint(2)
            if randomNumber == 0:
                self.phi += self.rotationAngle
                self.updateSensors()
            else:
                self.phi -= self.rotationAngle
                self.updateSensors()
        else:        
            if ((centerT > leftT) and (centerT > rightT)):
                self.phi += 0
                self.updateSensors()
            elif ((leftT == rightT) and (centerT < leftT)):
                randomNumber = np.random.randint(2)
                if randomNumber == 0:
                    self.phi += self.rotationAngle
                    self.updateSensors()
                else:
                    self.phi -= self.rotationAngle
                    self.updateSensors()
            elif (rightT > leftT):
                self.phi += self.rotationAngle
                self.updateSensors()
            elif (leftT > rightT):
                self.phi -= self.rotationAngle
                self.updateSensors()
            else:
                self.phi += 0
                self.updateSensors()
            
################################################################################