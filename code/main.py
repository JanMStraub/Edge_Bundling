# -*- coding: utf-8 -*-

"""
PolyCenterephalum simulation
Based on the work of:
* Jeff Jones, UWE https://uwe-repository.worktribe.com/output/980579
* Sage Jensen https://sagejenson.com/physarum
* Amitav Mitra https://github.com/ammitra/Physarum
* Liang Liu https://www.researchgate.net/publication/272393174_Physarum_Optimization_A_Biology-Inspired_Algorithm_for_the_Steiner_Tree_Problem_in_Networks
@author: Jan Straub
"""

# Imports
import os
import imageio
import random

from tqdm import tqdm

from environment import Environment
from helper import readGraphData
from simulation import physarumAlgorithm, initializePhysarium, updateCalculations
from debug import test


def main(jsonFile, steps, image, viscosity, initialFlow, sigma, rho, tau, sensorNodeList):

    # Import graph information from JSON
    edgeList, nodeList = readGraphData(jsonFile) 
    
    # Setup environment
    environment = Environment()
    environment.createGrid(nodeList)
    environment.createTerminalNodes(nodeList) 
    environment.createSensorNodes(sensorNodeList)
    
    # Setup simulation
    initializePhysarium(environment._edgeList, environment._nodeList, environment._terminalNodeList, environment._sensorNodeList, viscosity, initialFlow)
    
    if (image):

        for t in tqdm(range(steps), desc = "Iteration progress"):   
            
            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau)
            
            if t == steps - 1:
                plt = environment.plotGraph(t) 
                
                xList = []
                yList = []
                
                for sensor in environment._sensorNodeList:
                    x, y, z = sensor
                    xList.append(x)
                    yList.append(y)
    
                plt.plot(xList, yList, "go")
                plt.savefig("simulation_t{}.png".format(t + 1))
                plt.clf()
                
            tau = 0.0004 * t
            
    else:
        filenames = []
        
        for t in tqdm(range(steps), desc = "Iteration progress"):

            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau)
            
            
            if (t > 1200):
                plt = environment.plotGraph(t)
                filename = f'{t}.png'
                filenames.append(filename)
                
                plt.savefig(filename)
                plt.close()
        
             
            if t == steps - 1:
                plt = environment.plotGraph(t)
                filename = f'{t}.png'
                filenames.append(filename)
                
                plt.savefig(filename)
                plt.close()
                
                with imageio.get_writer("simulationGIF_t{}.gif".format(t + 1), mode='I') as writer:
                    for filename in filenames:
                        image = imageio.imread(filename)
                        writer.append_data(image)
                    
                # Remove files
                for filename in set(filenames):
                    os.remove(filename)
            
            tau = 0.0004 * t
            
    return


if __name__ == "__main__":

    # Setup parameter
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/2x2_test_graph.json" 
    steps = 3
    image = True # Change to False if you want a gif
    
    # Slime parameters
    viscosity = 0.5
    initialFlow = 0.5 
    sigma = 0.00000375
    rho = 0.0002
    tau = 0.0004
    
    sensorNodeList = [(0.1, 0.9, 0)]
    
    """
    (0.1, 0.9, 0)
    
    (2, 1.7, 0), (0, 1.7, 0), (2, 0.4999, 0), (0, 0.4999, 0)
    
    (0.75, 4.1, 0), (3.25, 4.1, 0), (2, 0.1, 0), (0.35, 2.55, 0), (3.656, 2.55, 0), (-0.3, 1.8, 0), (4.2, 1.8, 0), (-0.65, 0.6, 0), (4.7, 0.6, 0)
    
    (0, 12.1, 0), (0, 12.7, 0), (0.1, 13.3, 0), (1, 5.8, 0), (1.1, 18.1, 0), (1.2, 9, 0), (2.2, 11.1, 0), (2.2, 11.2, 0), (3, 16.4, 0), (3.2, 3.9, 0), (4.1, 4.9, 0), (4.3, 5.3, 0), (4.8, 15.6, 0), (4.8, 16.5, 0), (5.0, 14.1, 0), (5, 16.6, 0), (5.8, 9.1, 0), (5.7, 9.7, 0), (6.3, 8, 0), (6.2, 9.6, 0), (7, 15.1, 0), (7.2, 17, 0), (7.5, 1.4, 0), (8.8, 10.9, 0), (9.1, 16, 0), (8.9, 19.6, 0), (9.3, 6.8, 0), (10, 5.3, 0), (10.4, 2.9, 0), (10.2, 3.9, 0), (10.3, 4.8, 0), (11.1, 5, 0), (11, 8.1, 0), (11.1, 12.7, 0), (11, 16.2, 0), (13.1, 19.4, 0), (13.4, 15.6, 0), (13.7, 18.7, 0), (14.4, 7.5, 0), (14.2, 10.1, 0), (14.2, 16.8, 0), (16, 11.4, 0), (15.8, 12.7, 0), (15.4, 18.6, 0), (16.4, 17.4, 0), (17.1, 0.3, 0), (17.8, 1.2, 0), (18.2, 3.8, 0), (17.6, 6, 0), (17.6, 19.5, 0)
    """
    
    # main(jsonFile, steps, image, viscosity, initialFlow, sigma, rho, tau, sensorNodeList)
    test(jsonFile, steps, viscosity, initialFlow, sigma, rho, tau, sensorNodeList)