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

from environment import Environment
from helper import readGraphData
from simulation import calculateFlux


def main():
    
    # Setup parameter
    jsonFile = "code/data/simple_graph.json"
    N = 200
    M = 200
    viscosity = 4.5
    flux = 0
    steps = 1
    intervals = 8
    scale = 3
    image = True # Change to False if you want a gif
    
    # Import graph information from JSON
    edges, nodes, numberOfEdges, numberOfNodes = readGraphData(jsonFile) 
    
    # Setup environment
    environment = Environment(N, M)
    environment.createNodes(nodes)
    environment.createEdges(edges)
    environment.spawnNodes(scale)
    
    # testing
    # calculateFlux(environment._nodeList, environment._edgeList)
    
    
    if (image):
        dt = int(steps / intervals)
        
        for i in range(steps):   
            environment.spawnNodes(scale) # Nodes have to spawn each iteration because of decay
            
            print("Iteration: {}".format(i + 1))
            
            if i == steps - 1:
                fig = plt.figure(figsize = (10, 12), dpi = 200)
                ax = fig.add_subplot(111)
                ax.imshow(environment._trailMap)
                ax.set_title("Polycephalum Test, step = {}".format(i + 1))
                ax.text(0, -30, "Nodes: {} Edges: {}".format(numberOfNodes, numberOfEdges))
                plt.savefig("simulation_t{}.png".format(i + 1))
                plt.clf()
    else:
        ims = []
        fig = plt.figure(figsize = (10, 12), dpi = 100)
        ax = fig.add_subplot(111)
        
        for i in range(steps):
            environment.spawnNodes(scale)
            
            environment.motorStage()
            environment.sensoryStage()
            print("Iteration: {}".format(i + 1))
            
            txt = plt.text(0, -30, "iteration: {} Population: {} Nodes: {} Edges: {}".format(i + 1, len(environment._agents), numberOfNodes, numberOfEdges))
            im = plt.imshow(environment._trailMap, animated = True)
            ims.append([im, txt])
        
        fig.suptitle("Polycephalum Test")
        ani = animation.ArtistAnimation(fig, ims, interval = 50, blit = True, repeat_delay = 1000)
        ani.save("simulation.gif")
        
    return


if __name__ == "__main__":
    
    main()