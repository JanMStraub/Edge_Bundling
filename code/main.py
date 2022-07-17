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
    steps = 10
    intervals = 8
    scale = 3
    plot = False # Change to False if you want a gif
    
    # Import graph information from JSON
    edges, nodes, numberOfEdges, numberOfNodes = readGraphData(jsonFile) 
    
    # Setup environment
    environment = Environment(N, M)
    # environment.spawnAgents(sensorAngle, rotationAngle, sensorOffset)
    environment.createNodes(nodes)
    environment.createEdges(edges)
    environment.spawnNodes(scale)
    environment.spawnEdges(scale, sensorAngle, rotationAngle, sensorOffset)
    
    environment.spawnNegativNode((75, 75), strength = -5, radius = 15)
    
    if (plot):
        dt = int(steps / intervals)
        
        for i in range(steps):
            environment.diffusionOperator(decayRate, sigma)   
            environment.spawnNodes(scale) # Nodes have to spawn each iteration because of decay #TODO change that
            
            environment.motorStage()
            environment.sensoryStage()
            print("Iteration: {}".format(i))
            
            if i == steps - 1:
                fig = plt.figure(figsize = (8, 8), dpi = 200)
                ax = fig.add_subplot(111)
                ax.imshow(environment.trailMap)
                ax.set_title("Polycephalum Test, step = {}".format(i + 1))
                ax.text(0, -10, "Sensor Angle: {:.2f} Sensor Offset: {} Rotation Angle: {:.2f} Population: {}".format(np.degrees(sensorAngle), sensorOffset, np.degrees(rotationAngle), len(environment.agents)))
                plt.savefig("simulation_t{}.png".format(i))
                plt.clf()
    else:
        ims = []
        fig = plt.figure(figsize = (8, 8), dpi = 100)
        ax = fig.add_subplot(111)
        
        for i in range(steps):
            environment.diffusionOperator(decayRate, sigma)
            environment.spawnNodes(scale)
            
            environment.motorStage()
            environment.sensoryStage()
            print("Iteration: {}".format(i))
            
            txt = plt.text(0, -10, "iteration: {} Sensor Angle: {:.2f} Sensor Offset: {} Rotation Angle: {:.2f} Population: {}".format(i, np.degrees(sensorAngle), sensorOffset, np.degrees(rotationAngle), len(environment.agents)))
            im = plt.imshow(environment.trailMap, animated = True)
            ims.append([im, txt])
        
        fig.suptitle("Polycephalum Test")
        ani = animation.ArtistAnimation(fig, ims, interval = 50, blit = True, repeat_delay = 1000)
        ani.save("simulation.gif")
        
    return


if __name__ == "__main__":
    
    main()