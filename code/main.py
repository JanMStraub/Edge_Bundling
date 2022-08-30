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
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tqdm import tqdm

from environment import Environment
from helper import readGraphData
from simulation import physarumAlgorithm, initializePhysarium


def main():
    
    # Setup parameter
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/planar_graph.json"
    steps = 50000
    intervals = 8
    image = True # Change to False if you want a gif
    
    # Slime parameters
    viscosity = 1.0
    initialFlow = 10
    sigma = 0.000000375
    rho = 0.0002
    tau = 0.00000004
    edgeCost = 1
    
    # Import graph information from JSON
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile) 
    
    # Setup environment
    environment = Environment()
    environment.createNodes(nodeList)
    environment.createEdges(edgeList, edgeCost)
    
    # Setup simulation
    initializePhysarium(environment._nodeList, environment._edgeList, viscosity, initialFlow)
    
    if (image):
        dt = int(steps / intervals)
        
        for t in tqdm(range(steps), desc = "Iteration progress"):   
            
            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau) 
            
            if t == steps - 1:
                fig = plt.figure(figsize = (10, 10), dpi = 200)
                ax = fig.add_subplot(111)
                fig = environment.plotGraph(plt)
                ax.set_title("Polycephalum Test, step = {}".format(t + 1))
                plt.savefig("simulation_t{}.png".format(t + 1))
                plt.clf()
                
            tau = 0.000004 * t #00000004
            
    else:
        ims = []
        fig = plt.figure(figsize = (10, 10), dpi = 100)
        ax = fig.add_subplot(111)
        
        for t in tqdm(range(steps), desc = "Iteration progress"):
            
            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._edgeList, viscosity, initialFlow, sigma, rho, tau)            
            
            fig = environment.plotGraph(plt)
            txt = plt.text(0, -30, "iteration: {} Nodes: {} Edges: {}".format(t + 1, numberOfNodes, numberOfEdges))
            im = plt.plot()
            ims.append([im, txt])
            
            tau = 0.00000004 * t
        
        fig.suptitle("Polycephalum Test")
        ani = animation.ArtistAnimation(fig, ims, interval = 1000, blit = True, repeat_delay = 1000)
        ani.save("simulation.gif")
        
    return


if __name__ == "__main__":
    
    main()