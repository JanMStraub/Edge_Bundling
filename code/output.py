# -*- coding: utf-8 -*-

"""
This file manages the post-processing and plotting of the graph
@author: Jan Straub
"""

# Imports
from networkx import Graph
from networkx import get_node_attributes, shortest_path, draw, draw_networkx_nodes, draw_networkx_edge_labels, draw_networkx_labels
from scipy.interpolate import BPoly, splprep, splev
from numpy import asarray, linspace, arange

import matplotlib.pyplot as plt

from post_processing import remove_unused_grid_nodes, remove_nodes_within_radius, fermat_torricelli_point_calculation
from helper import find_path_nodes, find_node_by_id, calculate_edge_control_points, find_edge_between_nodes


def bezier_curve_calculation(networkxGraph, environmentNodeList,
                             environmentTerminalNodeList, environmentEdgeList,
                             pathList, smoothing):

    """_summary_
        Searches for path and calculates Bezier curve
    Args:
        networkxGraph (object): Graph created by networkx
        environmentNodeList (list): List of node objects
        environmentTerminalNodeList (list): List of terminal node objects
        environmentEdgeList (list): List of edge object in network
        pathList (list): List of path
        smoothing (int): A smoothing parameter for the Bezier curve bundling
    """

    bezierPointList = []

    for path in pathList:
        startPoint, endPoint = path
        finishedPathList, calculatedPathList = [], []
        startNode, endNode = None, None

        if [startPoint, endPoint] or [endPoint, startPoint] not in finishedPathList:
            finishedPathList.append(path)
            startNode, endNode = find_path_nodes(startPoint, endPoint,
                                                 environmentTerminalNodeList)

            calculatedPathList = shortest_path(networkxGraph,
                                               startNode.nodeObjectId,
                                               endNode.nodeObjectId)

        controlPoints = []
        calculatedPathList.pop(0)

        controlPoints.append(startNode.position)

        if smoothing > 0:
            lastNode = startNode
            for pathNode in calculatedPathList:
                nextNode = find_node_by_id(environmentNodeList, pathNode)
                for point in find_edge_between_nodes(environmentEdgeList,
                                                     lastNode, nextNode).edgeControlPointsList:
                    controlPoints.append(point)

                lastNode = nextNode

            controlPoints.append(endNode.position)
        else:
            for pathNode in calculatedPathList:
                controlPoints.append(find_node_by_id(environmentNodeList,
                                        pathNode).position)

        npControlPoints = asarray(controlPoints)

        curve = BPoly(npControlPoints[:, None, :], [0, 1])
        curvePoints = curve(linspace(0, 1, 100))

        bezierPointList.append(curvePoints.T)

    return bezierPointList


def cubic_spline_calculation(networkxGraph, environmentNodeList,
                             environmentTerminalNodeList, environmentEdgeList,
                             pathList, smoothing):

    """_summary_
        Searches for path and calculates cubic spline curve
    Args:
        networkxGraph (object): Graph created by networkx
        environmentNodeList (list): List of node objects
        environmentTerminalNodeList (list): List of terminal node objects
        environmentEdgeList (list): List of edge object in network
        pathList (list): List of path
        smoothing (int): A smoothing parameter for the Bezier curve bundling
    """

    cubicSplineList = []

    for path in pathList:
        startPoint, endPoint = path
        finishedPathList, calculatedPathList = [], []
        startNode, endNode = None, None

        if [startPoint, endPoint] or [endPoint, startPoint] not in finishedPathList:
            finishedPathList.append(path)
            startNode, endNode = find_path_nodes(startPoint, endPoint,
                                                 environmentTerminalNodeList)

            calculatedPathList = shortest_path(networkxGraph,
                                               startNode.nodeObjectId,
                                               endNode.nodeObjectId)

        controlPoints = []
        calculatedPathList.pop(0)

        controlPoints.append(startNode.position)

        if smoothing > 0:
            lastNode = startNode
            for pathNode in calculatedPathList:
                nextNode = find_node_by_id(environmentNodeList, pathNode)
                for point in find_edge_between_nodes(environmentEdgeList,
                                                     lastNode, nextNode).edgeControlPointsList:
                    controlPoints.append(point)

                lastNode = nextNode

            controlPoints.append(endNode.position)

            npControlPoints = asarray(controlPoints)

            tck = splprep(npControlPoints.transpose(), s = 0)[0]
            unew = arange(0, 1.01, 0.01)
            cubicSplineList.append(splev(unew, tck))

        else:
            raise ValueError ("Cubic spline plot must have SMOOTHING factor of at least 1")

    return cubicSplineList

def plot_graph(path, jsonFileName, outerIteration, innerIteration,
               savedNetwork, pathList, smoothing,
               postProcessingSelection):

    """_summary_
        Plot edges and nodes in matplotlib
    Args:
        path (string): Path for plot save
        jsonFileName (sting): Name of file
        outerIteration (int): Number of outer iterations
        innerIteration (int): Number of inner iterations
        savedNetwork (object): Network that has the lowest cost
        pathList (list): List of original paths
        smoothing (int): A smoothing parameter for the Bezier curve bundling
        postProcessingSelection (int): Selection which postprocessing should be used
    """

    environmentNodeList = savedNetwork.environmentNodeList
    environmentTerminalNodeList = savedNetwork.environmentTerminalNodeList
    environmentEdgeList = savedNetwork.environmentEdgeList

    removeEdge = savedNetwork.remove_edge
    createSteinerEdge = savedNetwork.create_steiner_edge

    remove_unused_grid_nodes(environmentNodeList,
                             environmentTerminalNodeList,
                             removeEdge, createSteinerEdge,
                             environmentEdgeList)

    fermat_torricelli_point_calculation(environmentNodeList)

    remove_nodes_within_radius(environmentNodeList, removeEdge,
                               createSteinerEdge)

    networkxGraph, sizeValues, nodeLabels = Graph(), [], {}

    for node in environmentNodeList:
        x, y = node.position
        networkxGraph.add_node(node.nodeObjectId, pos = (x, y))

        if node in environmentTerminalNodeList:
            nodeLabels[node.nodeObjectId] = node.nodeObjectId
            sizeValues.append(200)
        else:
            nodeLabels[node.nodeObjectId] = node.nodeObjectId
            sizeValues.append(200)

    if postProcessingSelection == 0:
        plot = plot_steiner_graph(outerIteration, innerIteration,
                                 environmentEdgeList, networkxGraph,
                                 sizeValues, nodeLabels)

    elif postProcessingSelection == 1:
        plot = plot_bezier_graph(outerIteration, innerIteration,
                                environmentEdgeList,
                                environmentNodeList,
                                environmentTerminalNodeList,
                                networkxGraph,
                                pathList, smoothing, sizeValues)

    elif postProcessingSelection == 2:
        plot = plot_cubic_spline_graph(outerIteration, innerIteration,
                                      environmentEdgeList,
                                      environmentNodeList, environmentTerminalNodeList,
                                      networkxGraph,
                                      pathList, smoothing, sizeValues)

    else:
        raise ValueError(f"postProcessingSelection value {postProcessingSelection} is not defined")

    plot.tight_layout()
    plot.savefig(path + f"/plots/{jsonFileName}_{outerIteration}-{innerIteration}.png")
    plot.clf()


def plot_steiner_graph(outerIteration, innerIteration,
                       environmentEdgeList, networkxGraph,
                       sizeValues, nodeLabels):

    """_summary_
        Creates Steiner graph
    Args:
        outerIteration (int): Number of outer iterations
        innerIteration (int): Number of inner iterations
        environmentEdgeList (list): List of all edge objects
        networkxGraph (object): Graph created by networkx
        sizeValues (list): List of node size values
        nodeLabels (dict): Dict of node ids

    Returns:
        plt (object): Matplotlib object
    """

    for edge in environmentEdgeList:
        networkxGraph.add_edge(edge.start.nodeObjectId, edge.end.nodeObjectId)

    fig = plt.figure()
    fig = plt.figure(figsize = (10, 10))
    subplot = fig.add_subplot(111)
    subplot.set_title(f"Polycephalum Edge Bundling - out: {outerIteration} - in: {innerIteration}")

    pos = get_node_attributes(networkxGraph, 'pos')
    draw(networkxGraph, pos, node_size = sizeValues)
    draw_networkx_nodes(networkxGraph, pos, node_size = sizeValues)
    draw_networkx_labels(networkxGraph, pos, nodeLabels)

    return plt


def plot_bezier_graph(outerIteration, innerIteration,
                      environmentEdgeList,
                      environmentNodeList,
                      environmentTerminalNodeList,
                      networkxGraph,
                      pathList, smoothing, sizeValues):

    """_summary_
        Create Bezier curve plot
    Args:
        outerIteration (int): Number of outer iterations
        innerIteration (int): Number of inner iterations
        environmentEdgeList (list): List of all edge objects
        environmentNodeList (list): List of node objects
        environmentTerminalNodeList (list): List of terminal node objects
        networkxGraph (object): Graph created by networkx
        pathList (list): List of original paths
        smoothing (int): A smoothing parameter for the Bezier curve bundling
        sizeValues (list): List of node size values

    Returns:
        plt (object): Matplotlib object
    """

    calculate_edge_control_points(environmentEdgeList, smoothing)

    for edge in environmentEdgeList:
        networkxGraph.add_edge(edge.start.nodeObjectId, edge.end.nodeObjectId)

    bezierPointList = bezier_curve_calculation(networkxGraph,
                                               environmentNodeList,
                                               environmentTerminalNodeList,
                                               environmentEdgeList,
                                               pathList, smoothing)

    fig = plt.figure()
    fig = plt.figure(figsize = (10, 10))
    subplot = fig.add_subplot(111)
    subplot.set_title(f"Polycephalum Edge Bundling - out: {outerIteration} - in: {innerIteration}")

    for bezierCurve in bezierPointList:
        plt.plot(*bezierCurve, color="black")

    pos = get_node_attributes(networkxGraph, 'pos')
    draw_networkx_nodes(networkxGraph, pos, node_size = sizeValues)

    return plt


def plot_cubic_spline_graph(outerIteration, innerIteration,
                            environmentEdgeList, environmentNodeList,
                            environmentTerminalNodeList, networkxGraph,
                            pathList, smoothing, sizeValues):

    """_summary_
        Create cubic spline curve plot
    Args:
        outerIteration (int): Number of outer iterations
        innerIteration (int): Number of inner iterations
        environmentEdgeList (list): List of all edge objects
        environmentNodeList (list): List of node objects
        environmentTerminalNodeList (list): List of terminal node objects
        networkxGraph (object): Graph created by networkx
        pathList (list): List of original paths
        smoothing (int): A smoothing parameter for the Bezier curve bundling
        sizeValues (list): List of node size values

    Returns:
        plt (object): Matplotlib object
    """

    calculate_edge_control_points(environmentEdgeList, smoothing)

    for edge in environmentEdgeList:
        networkxGraph.add_edge(edge.start.nodeObjectId, edge.end.nodeObjectId)

    cubicSplineList = cubic_spline_calculation(networkxGraph,
                                               environmentNodeList,
                                               environmentTerminalNodeList,
                                               environmentEdgeList,
                                               pathList, smoothing)

    fig = plt.figure()
    fig = plt.figure(figsize = (10, 10))
    subplot = fig.add_subplot(111)
    subplot.set_title(f"Polycephalum Edge Bundling - out: {outerIteration} - in: {innerIteration}")

    for cubicSpline in cubicSplineList:
        plt.plot(cubicSpline[0], cubicSpline[1], color = "black")

    pos = get_node_attributes(networkxGraph, 'pos')
    draw_networkx_nodes(networkxGraph, pos, node_size = sizeValues)

    return plt
