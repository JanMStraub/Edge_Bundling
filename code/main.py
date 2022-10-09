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


def main(jsonFile, N, image, viscosity, initialFlow, mu, epsilon, K, alpha):

    # Import graph information from JSON
    edgeList, nodeList = readGraphData(jsonFile) 
     
    if (image):
        totalCost = [10000000] * 2
        savedNetwork = None

        for t in tqdm(range(N), desc = "Outer iteration progress"):   
            
            # Setup environment
            environment = Environment()
            environment.createGrid(nodeList)
            
            # Start simulation
            # totalCost[1] = physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, mu, epsilon, K, alpha)
            
            if (totalCost[0] > totalCost[1]):
                savedNetwork = environment
                totalCost[0] = totalCost[1]
            
            if n == N - 1:
                plt = environment.plotGraph(t, epsilon) 
                plt.savefig("simulation_t{}.png".format(n + 1))
                plt.clf()
                
            # epsilon = 0.0004 * n
            
    else:
        filenames = []
        
        for n in tqdm(range(N), desc = "Outer iteration progress"):

            # Start simulation
            physarumAlgorithm(environment._nodeList, environment._terminalNodeList, environment._edgeList, viscosity, initialFlow, mu, epsilon, K, alpha)
            
            
            if (n >= 1569) and (n <= 1598):
                plt = environment.plotGraph(n)
                filename = f'{n}.png'
                filenames.append(filename)
                
                plt.savefig(filename)
                plt.close()
        
            if n == N - 1:
                plt = environment.plotGraph(n, epsilon)
                filename = f'{n}.png'
                filenames.append(filename)
                
                plt.savefig(filename)
                plt.close()
                
                with imageio.get_writer("simulationGIF_t{}.gif".format(n + 1), mode='I') as writer:
                    for filename in filenames:
                        image = imageio.imread(filename)
                        writer.append_data(image)
                    
                # Remove files
                for filename in set(filenames):
                    os.remove(filename)
            
            epsilon = 0.0004 * n
            
    return


if __name__ == "__main__":

    # Setup parameter
    jsonFile = "/Users/jan/Documents/code/bachelor_thesis/code/data/3x3_test_graph.json" 
    N = 1 # 1238 
    K = 15
    image = True # Change to False if you want a gif
    
    # Slime parameters
    viscosity = 0.5
    initialFlow = 1
    mu = 1
    epsilon = 0.001
    alpha = 0.4
    
    # main(jsonFile, N, image, viscosity, initialFlow, mu, epsilon, K, alpha)
    test(jsonFile, N, viscosity, initialFlow, mu, epsilon, K, alpha)