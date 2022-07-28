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
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from environment import Environment
from helper import readGraphData


def main():
    
    # Setup parameter
    jsonFile = "code/data/simple_graph.json"
    N = 200
    M = 200
    sensorAngle = np.pi / 4 # 22.5 or 45 angle
    rotationAngle = np.pi / 4
    sensorOffset = 9
    decayRate = 0.85
    sigma = 0.65
    steps = 250
    intervals = 8
    scale = 3
    image = True # Change to False if you want a gif
    
    # Import graph information from JSON
    edges, nodes, numberOfEdges, numberOfNodes = readGraphData(jsonFile) 
    
    # Setup environment
    environment = Environment(N, M)
    # environment.spawnAgents(sensorAngle, rotationAngle, sensorOffset)
    environment.createNodes(nodes)
    environment.spawnOffLimitNode((50, 70), strength = -1, radius = 10)
    environment.createEdges(edges)
    environment.spawnNodes(scale)
    environment.spawnEdges(scale, sensorAngle, rotationAngle, sensorOffset)
    
    
    if (image):
        dt = int(steps / intervals)
        
        for i in range(steps):
            environment.diffusionOperator(decayRate, sigma)   
            environment.spawnNodes(scale) # Nodes have to spawn each iteration because of decay #TODO change that
            
            environment.motorStage()
            environment.sensoryStage()
            print("Iteration: {}".format(i + 1))
            
            if i == steps - 1:
                fig = plt.figure(figsize = (10, 12), dpi = 200)
                ax = fig.add_subplot(111)
                ax.imshow(environment.trailMap)
                # ax.imshow(environment.controlMap)
                ax.set_title("Polycephalum Test, step = {}".format(i + 1))
                ax.text(0, -30, "Sensor Angle: {:.2f} Sensor Offset: {} Rotation Angle: {:.2f} Population: {} Nodes: {} Edges: {}".format(np.degrees(sensorAngle), sensorOffset, np.degrees(rotationAngle), len(environment.agents), numberOfNodes, numberOfEdges))
                plt.savefig("simulation_t{}.png".format(i + 1))
                plt.clf()
    else:
        ims = []
        fig = plt.figure(figsize = (10, 12), dpi = 100)
        ax = fig.add_subplot(111)
        
        for i in range(steps):
            environment.diffusionOperator(decayRate, sigma)
            environment.spawnNodes(scale)
            
            environment.motorStage()
            environment.sensoryStage()
            print("Iteration: {}".format(i + 1))
            
            txt = plt.text(0, -30, "iteration: {} Sensor Angle: {:.2f} Sensor Offset: {} Rotation Angle: {:.2f} Population: {} Nodes: {} Edges: {}".format(i + 1, np.degrees(sensorAngle), sensorOffset, np.degrees(rotationAngle), len(environment.agents), numberOfNodes, numberOfEdges))
            im = plt.imshow(environment.trailMap, animated = True)
            ims.append([im, txt])
        
        fig.suptitle("Polycephalum Test")
        ani = animation.ArtistAnimation(fig, ims, interval = 50, blit = True, repeat_delay = 1000)
        ani.save("simulation.gif")
        
    return


if __name__ == "__main__":
    
    main()