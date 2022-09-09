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

import matplotlib.pyplot as plt

from tqdm import tqdm
from PIL import Image, ImageDraw

from environment import Environment
from helper import readGraphData
from simulation import physarumAlgorithm, initializePhysarium


def main():
    
    # Setup parameter
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/5x5_test_graph.json" 
    steps = 700 #734
    image = True # Change to False if you want a gif
    
    # Slime parameters
    viscosity = 1.0
    initialFlow = 1.0 
    sigma = 0.000000375
    rho = 0.0002
    tau = 0.0004 
    
    # Import graph information from JSON
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile) 
    
    print("Number of nodes: " + str(numberOfNodes))
    print("Number of edges: " + str(numberOfEdges))
    
    # Setup environment
    environment = Environment()
    environment.createGrid(nodeList)
    environment.createTerminalNodes(nodeList) 
    
    # Setup simulation
    initializePhysarium(environment._edgeList, environment._nodeList, environment._terminalNodeList, viscosity, initialFlow)
    
    if (image):

        for t in tqdm(range(steps), desc = "Iteration progress"):   
            
            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau)

            if t == steps - 1:
                plt = environment.plotGraph(t) 
                plt.savefig("simulation_t{}.png".format(t + 1))
                plt.clf()
                
            tau = 0.0004 * t #00000004
            
    else:
        filenames = []
        
        for t in tqdm(range(steps), desc = "Iteration progress"):
            
            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau)
            
            
            if (t > 0):
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
            
            tau = 0.0004 * t #00000004
        
    return


if __name__ == "__main__":
    
    main()