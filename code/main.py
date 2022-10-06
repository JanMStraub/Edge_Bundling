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

from tqdm import tqdm

from environment import Environment
from helper import readGraphData
from simulation import physarumAlgorithm
from debug import test


def main(jsonFile, steps, image, viscosity, initialFlow, mu, epsilon, K):

    # Import graph information from JSON
    edgeList, nodeList = readGraphData(jsonFile) 
     
    if (image):
        totalCost = [10000000] * 2
        savedNetwork = None

        for t in tqdm(range(steps), desc = "Outer iteration progress"):   
            
            # Setup environment
            environment = Environment()
            environment.createGrid(nodeList)
            
            # Start simulation
            totalCost[1] = physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, mu, epsilon, K)
            
            if (totalCost[0] > totalCost[1]):
                savedNetwork = environment
                totalCost[0] = totalCost[1]
            
            if t == steps - 1:
                plt = savedNetwork.plotGraph(t, epsilon) 
                plt.savefig("simulation_t{}.png".format(t + 1))
                plt.clf()
                
            # epsilon = 0.0004 * t
            
    else:
        filenames = []
        
        for t in tqdm(range(steps), desc = "Outer iteration progress"):

            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, mu, epsilon, K)
            
            
            if (t >= 1569) and (t <= 1598):
                plt = environment.plotGraph(t)
                filename = f'{t}.png'
                filenames.append(filename)
                
                plt.savefig(filename)
                plt.close()
        
             
            if t == steps - 1:
                plt = environment.plotGraph(t, epsilon)
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
            
            epsilon = 0.0004 * t
            
    return


if __name__ == "__main__":

    # Setup parameter
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/3x3_test_graph.json" 
    steps = 1 # 1238 
    K = 10
    image = True # Change to False if you want a gif
    
    # Slime parameters
    viscosity = 0.5
    initialFlow = 1
    mu = 1
    epsilon = 0.001
    
    # main(jsonFile, steps, image, viscosity, initialFlow, mu, epsilon, K)
    test(jsonFile, steps, viscosity, initialFlow, mu, epsilon, K)