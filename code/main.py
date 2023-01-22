# -*- coding: utf-8 -*-

"""
Edge bundling algorithm with Physarum polycephalum approximations of Steiner trees
@author: Jan Straub
"""

# Imports
from os import remove
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from pickle import dump, load
from imageio import imread, get_writer

import matplotlib.pyplot as plt

from environment import ENVIRONMENT
from helper import read_graph_data, get_min_max_values, minimum_spanning_tree_length
from simulation import physarum_algorithm
from output import plot_graph


def start(nodeList, xMin, xMax, yMin, yMax,
        viscosity, initialFlow, mu, epsilon,
        innerIteration, alpha, edgeAlpha):
    """_summary_
        Start function for multiprocessing
    Args:
        nodeList (list): List of node objects
        xMin (float): Minimal x value of original nodes
        xMax (float): Maximum x value of original nodes
        yMin (float): Minimal y value of original nodes
        yMax (float): Maximum y value of original nodes
        viscosity (float): The viscosity of the fluid inside the network
        initialFlow (int): The initial flow of the fluid
        mu (int): A constant
        epsilon (float): Coductivity threshold
        innerIteration (int): Number of inner iterations
        alpha (float): A positiv constant
        edgeAlpha (float): A positiv constant for each edge

    Returns:
        totalEdgeCost (float): Total cost of the network
        steinerConnections (bool): If only Steiner connections are present
        environment (object): Network object
    """

    # Setup environment
    environment = ENVIRONMENT(nodeList, xMin, xMax, yMin, yMax,
                              viscosity)

    # Start simulation
    totalCost, steinerConnections = physarum_algorithm(
        environment.environmentNodeList,
        environment.environmentTerminalNodeList,
        environment.environmentEdgeList,
        initialFlow, mu, epsilon, innerIteration,
        alpha, edgeAlpha)

    return totalCost, steinerConnections, environment


def main(path, jsonFile, plotSelection, postProcessingSelection,
         viscosity, initialFlow, mu, epsilon,
         alpha, edgeAlpha, smoothing):

    """_summary_
        This is the main function of the algorithm
    Args:
        path (string): The path where the code is based
        jsonFile (string): Path to json file
        plotSelection (int): What mode the algorithm should run
            0 new calculation - 1 plot saved network - 2 plot gif
        postProcessingSelection (int): Selection which postprocessing should be used
            0 Steiner tree - 1 Bezier curve - 2 cubic spline
        viscosity (float): The viscosity of the fluid inside the network
        initialFlow (int): The initial flow of the fluid
        mu (int): A constant
        epsilon (float): Coductivity threshold
        alpha (float): A positiv constant
        edgeAlpha (float): A positiv constant for each edge
        smoothing (int): A smoothing parameter for the Bezier curve bundling
    """

    # Import graph information from JSON
    nodeList, pathList = read_graph_data(jsonFile)
    xMin, xMax, yMin, yMax = get_min_max_values(nodeList)
    bestCostList = [minimum_spanning_tree_length(nodeList, pathList)]
    xAxis, yAxis = int((xMax - xMin) + 1), int((yMax - yMin) + 1)

    # Outer and inner iteration bound
    if xAxis >= yAxis:
        outerIteration = xAxis * cpu_count()
        innerIteration = xAxis ** 4
    elif xAxis < yAxis:
        outerIteration = yAxis * cpu_count()
        innerIteration = yAxis ** 4

    print(f"xAxis: {xAxis} - "
          f"yAxis: {yAxis} - "
          f"outerIteration: {outerIteration} - "
          f"innerIteration: {innerIteration}")

    if plotSelection == 0:
        savedNetwork, results = None, None
        currentOuterIterations = outerIteration

        while savedNetwork is None:
            with ProcessPoolExecutor() as executor:

                # Start simulation
                results = [executor.submit(start, nodeList,
                                        xMin, xMax, yMin, yMax,
                                        viscosity, initialFlow,
                                        mu, epsilon, innerIteration,
                                        alpha, edgeAlpha)
                        for _ in range(outerIteration)]

                for item in as_completed(results):
                    totalCost, steinerConnections, environment = item.result()
                    if bestCostList[-1] >= totalCost and steinerConnections:
                        savedNetwork = environment
                        bestCostList.append(totalCost)

            # Saveguard if no network is found yet
            if savedNetwork is None:
                innerIteration = int(innerIteration * 1.5)
                outerIteration = cpu_count()
                currentOuterIterations += outerIteration

        with open(path +
                    f"/savedNetworks/simulation_{currentOuterIterations} - {innerIteration}.obj",
                    mode = "wb") as fileDebug:
            dump(savedNetwork, fileDebug)

        plot_graph(path, currentOuterIterations, innerIteration,
                    savedNetwork, pathList, smoothing, postProcessingSelection)

    if plotSelection == 1:

        with open(path +
                  f"/savedNetworks/simulation_{outerIteration} - {innerIteration}.obj",
                  mode = "rb") as fileDebug:
            savedNetwork = load(fileDebug)

        plot_graph(path, outerIteration, innerIteration,
                   savedNetwork, pathList, smoothing, postProcessingSelection)

    if plotSelection == 2:
        bestCostList = [minimum_spanning_tree_length(nodeList, pathList)]
        savedNetwork = None
        n = 0
        filenameList = []


        for n in range(outerIteration):

            # Setup environment
            environment = ENVIRONMENT(nodeList, xMin, xMax, yMin, yMax,
                                      viscosity)

            # Start simulation
            totalCost, steinerConnections = physarum_algorithm(
                environment.environmentNodeList,
                environment.environmentTerminalNodeList,
                environment.environmentEdgeList,
                initialFlow, mu, epsilon, innerIteration,
                alpha, edgeAlpha)

            if bestCostList[-1] >= totalCost and steinerConnections:
                savedNetwork = environment
                bestCostList.append(totalCost)

            # Saveguard if no network is found yet
            if savedNetwork is None and n == outerIteration - 2:
                outerIteration += 1

            # Change mod for gif step size
            if n % 10 == 0:
                plot_graph(path, outerIteration, innerIteration,
                           savedNetwork, pathList, smoothing,
                           postProcessingSelection)

                filename = f'{n}.png'
                filenameList.append(filename)

                plt.savefig(filename)
                plt.close()

            if n == outerIteration - 1:
                plot_graph(path, outerIteration, innerIteration,
                           savedNetwork, pathList, smoothing,
                           postProcessingSelection)

                filename = f'{n}.png'
                filenameList.append(filename)

                plt.savefig(filename)
                plt.close()

                with get_writer(path + f"/plots/simulation_t{n + 1}.gif", mode='I') as writer:
                    for filename in filenameList:
                        image = imread(filename)
                        writer.append_data(image)

                # Remove files
                for filename in set(filenameList):
                    remove(filename)


if __name__ == "__main__":

    # Setup parameter
    PATH = "/Users/jan/Documents/code/gitlab_BA/2023-jan-straub"
    JSON_FILE = PATH + "/data/default.json"
    # 0 new calculation - 1 plot saved network - 2 plot gif
    PLOT_SELECTION = 1
    # 0 Steiner tree - 1 Bezier curve - 2 cubic spline
    POST_PROCESSING_SELECTION = 2

    # Slime parameters
    VISCOSITY = 0.5
    INITIAL_FLOW = 1
    MU = 1
    EPSILON = 0.001
    ALPHA = 0.4
    EDGE_ALPHA = 1.5
    SMOOTHING = 1

    main(PATH, JSON_FILE, PLOT_SELECTION, POST_PROCESSING_SELECTION,
         VISCOSITY, INITIAL_FLOW, MU, EPSILON,
         ALPHA, EDGE_ALPHA, SMOOTHING)
