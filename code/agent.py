# -*- coding: utf-8 -*-

# Imports
import numpy as np

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