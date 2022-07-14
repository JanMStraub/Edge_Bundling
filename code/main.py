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

from environment import Environment, Node
from helper import readGraphData


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
    scale = 3
    
    ### Change to False if you want a gif ###
    plot = True
    
    edges, nodes, numberOfEdges, numberOfNodes = readGraphData(jsonFile)
    
    environment = Environment(N, M, populationPercentage)
    #environment.spawnAgents(sensorAngle, rotationAngle, sensorOffset)
    environment.createNodes(nodes)
    environment.createEdges(edges)
    environment.spawnNodes(scale)
    environment.spawnEdges(sensorAngle, rotationAngle, sensorOffset)
    print(len(environment.agents))
    
    if (plot):
        dt = int(steps / intervals)
        samples = np.linspace(0, dt * intervals, intervals + 1)
        
        for i in range(steps):
            environment.diffusionOperator(decayRate, sigma)   
            environment.spawnNodes(scale)
            
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