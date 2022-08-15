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
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tqdm import tqdm
from time import sleep

from environment import Environment
from helper import readGraphData
from simulation import physarumAlgorithm, initializePhysarium


def main():
    
    # Setup parameter
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/simple_graph.json"
    N = 200
    M = 200
    steps = 10
    intervals = 8
    scale = 3
    image = True # Change to False if you want a gif
    
    # Slime parameters
    viscosity = 1.0
    initialFlow = 10.0
    sigma = 0.000000375
    rho = 0.0002
    edgeCost = 1
    
    # Import graph information from JSON
    edgeList, nodeList, numberOfEdges, numberOfNodes = readGraphData(jsonFile) 
    
    # Setup environment
    environment = Environment(N, M)
    environment.createNodes(nodeList)
    environment.createEdges(edgeList, edgeCost)
    environment.spawnNodes(scale, 3)
    environment.spawnEdges(scale)
    
    # Setup simulation
    initializePhysarium(environment._nodeList, environment._edgeList, viscosity = 1.0, initialFlow = 10.0)
    
    if (image):
        dt = int(steps / intervals)
        
        for i in tqdm(range(steps), desc="Iteration progress"):   
            
            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._edgeList, viscosity, initialFlow, sigma, rho)
            
            if i == steps - 1:
                fig = plt.figure(figsize = (10, 12), dpi = 200)
                ax = fig.add_subplot(111)
                ax.imshow(environment._dataMap)
                ax.set_title("Polycephalum Test, step = {}".format(i + 1))
                ax.text(0, -30, "Nodes: {} Edges: {}".format(numberOfNodes, numberOfEdges))
                plt.savefig("simulation_t{}.png".format(i + 1))
                plt.clf()
            
    else:
        ims = []
        fig = plt.figure(figsize = (10, 12), dpi = 100)
        ax = fig.add_subplot(111)
        
        for i in tqdm(range(steps), desc="Iteration progress"):
            
            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._edgeList, viscosity, initialFlow, sigma, rho)            
            
            print("Iteration: {}".format(i + 1))
            
            txt = plt.text(0, -30, "iteration: {} Population: {} Nodes: {} Edges: {}".format(i + 1, len(environment._agents), numberOfNodes, numberOfEdges))
            im = plt.imshow(environment._trailMap, animated = True)
            ims.append([im, txt])
            
            sleep(.1)
        
        fig.suptitle("Polycephalum Test")
        ani = animation.ArtistAnimation(fig, ims, interval = 50, blit = True, repeat_delay = 1000)
        ani.save("simulation.gif")
        
    return


if __name__ == "__main__":
    
    main()