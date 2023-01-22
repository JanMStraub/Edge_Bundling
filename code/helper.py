# -*- coding: utf-8 -*-

"""
This file contains helper functions
@author: Jan Straub
"""

# Imports
from json import load
from math import pi, dist, cos, acos
from networkx import Graph, minimum_spanning_tree
from numpy import linspace

def read_graph_data(path):

    """_summary_
        Function for reading JSON file and converting string data to tupel
    Returns:
        nodeList (list): A list of the original nodes positions
        paths (list) : A list of the original paths
    """

    # read graph data from JSON
    with open(path, mode = "r", encoding = "utf-8") as file:
        data = load(file)

    # Read relevant data
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
    paths = data["graph"]["edges"]

    nodeList = []
    nodeListAppend = nodeList.append

    # Convert node to tupel
    for i in range(len(nodes)):
        nodePosition = tuple(map(float, nodes[str(i)].strip("()").split(",")))
        nodeListAppend(nodePosition[:2])

    return nodeList, paths


def calculate_distance_between_positions(position1, position2):

    """_summary_
        Calculates the distance between two nodes
    Returns:
        dist (float): Distance between position1 and position2
    """

    return dist(position1, position2)


def find_node_by_position(environmentNodeList, x, y):

    """_summary_
        Function used to specific node object in node grid
    Returns:
        nodeAtPosition (object): Node object at position
    """

    nodeAtPosition = None

    for node in environmentNodeList:
        nodeX, nodeY = node.position
        if nodeX == x and nodeY == y:
            nodeAtPosition = node
            break

    return nodeAtPosition


def find_other_edge_end(node, edge):

    """_summary_
        Function used to find the other end of an edge
    Raises:
        ValueError: If edge has no end that can be found

    Returns:
        edge.end (object): Node object at the other end of the edge
        edge.start (object): Node object at the other end of the edge
    """

    if edge.start.nodeObjectId == node.nodeObjectId:
        return edge.end

    if edge.end.nodeObjectId == node.nodeObjectId:
        return edge.start

    raise ValueError(f"No end to edge {edge.edgeObjectId} found")


def get_min_max_values(nodeList):

    """_summary_
        Function returns min and max values of the original nodes
    Returns:
        xMin (float): Minimal x value of original nodes
        xMax (float): Maximum x value of original nodes
        yMin (float): Minimal y value of original nodes
        yMax (float): Maximum y value of original nodes
    """

    xMin, yMin = float("inf"), float("inf")
    xMax, yMax = 0.0, 0.0

    for node in nodeList:
        x, y = node

        if x < xMin:
            xMin = x
        if x > xMax:
            xMax = x

        if y < yMin:
            yMin = y
        if y > yMax:
            yMax = y

    return xMin, xMax, yMin, yMax


def minimum_spanning_tree_length(jsonNodeList, jsonPathList):

    """_summary_
        Calculates minimum spanning tree as a reference point for the graph length
    Args:
        jsonNodeList (list): A list of the original nodes positions
        jsonPathList (list): A list of the original paths

    Returns:
        minimumSpanningTree (float): Length of the minimum spanning tree
    """

    networkxGraph = Graph()

    graphAddNode = networkxGraph.add_node
    graphAddEdge = networkxGraph.add_edge

    for index, node in enumerate(jsonNodeList):
        x, y = node
        graphAddNode(index,
                     pos = (x, y))

    for edge in jsonPathList:
        graphAddEdge(edge[0], edge[1],
                     weight = calculate_distance_between_positions(
                         jsonNodeList[edge[0]], jsonNodeList[edge[1]]))

    minimumSpanningTree = minimum_spanning_tree(networkxGraph)

    return minimumSpanningTree.size()


def calculate_sides(A, B, C):

    """_summary_
        Given the points, returns the sides
    Args:
        A (list): Coordinates of point
        B (list): Coordinates of point
        C (list): Coordinates of point

    Returns:
        a (float): Distance between points
        b (float): Distance between points
        c (float): Distance between points
    """

    a = calculate_distance_between_positions(B, C)
    b = calculate_distance_between_positions(C, A)
    c = calculate_distance_between_positions(A, B)

    return a, b, c


def calculte_angle(a, b, c):

    """_summary_
        Given the sides, returns the angle
    Args:
        a (float): Distance between points
        b (float): Distance between points
        c (float): Distance between points

    Returns:
        angle (float): Angle between sides
    """

    return acos((b * b + c * c - a * a) / (2 * b * c))


def calculate_secant(a, b, c):

    """_summary_
        Given the sides, returns secant of that angle
    Args:
        a (float): Distance between points
        b (float): Distance between points
        c (float): Distance between points

    Returns:
        secant (float): Secant of the angle
    """

    return 1 / cos(calculte_angle(a, b, c) - pi / 6)


def calculate_coordinates(A, B, C, p, q, r):

    """_summary_
        Given the sides and the Trilinear co-ordinates, returns the Cartesian coordinates
    Args:
        A (list): Coordinates of point
        B (list): Coordinates of point
        C (list): Coordinates of point
        p (float): Distance times secant
        q (float): Distance times secant
        r (float): Distance times secant

    Returns:
        coordinates (list): Coordinates of Fermat point
    """

    return [(p * A[i] + q * B[i] + r * C[i]) / (p + q + r) for i in [0, 1]]


def fermat_point(A, B, C):

    """_summary_
        Checks if any of the angle is >= 2π/3 returns that point else computes the point
    Args:
        A (list): Coordinates of point
        B (list): Coordinates of point
        C (list): Coordinates of point

    Returns:
        Fermat point (list): Coordinates of Fermat point
    """

    if calculte_angle(*calculate_sides(A, B, C)) >= 2 * pi / 3:
        return A

    if calculte_angle(*calculate_sides(B, C, A)) >= 2 * pi / 3:
        return B

    if calculte_angle(*calculate_sides(C, A, B)) >= 2 * pi / 3:
        return C

    return calculate_coordinates(A, B, C,
                                 calculate_distance_between_positions(B, C) * calculate_secant(*calculate_sides(A, B, C)),
                                 calculate_distance_between_positions(C, A) *
                                 calculate_secant(*calculate_sides(B, C, A)),
                                 calculate_distance_between_positions(A, B) *
                                 calculate_secant(*calculate_sides(C, A, B)))


def find_path_nodes(startPoint, endPoint,
                    environmentTerminalNodeList):

    """_summary_
        Find node objects for path calculation
    Args:
        startPoint (int): Point id
        endPoint (int): Point id
        environmentTerminalNodeList (list): List of terminal node objects

    Returns:
        startNode (object): Start node object of path
        endNode (object): End node object of path
    """

    startNode, endNode = None, None
    for terminalNode in environmentTerminalNodeList:

        if startPoint == terminalNode.terminalNodeId:
            startNode = terminalNode

        if endPoint == terminalNode.terminalNodeId:
            endNode = terminalNode

    return startNode, endNode


def find_node_by_id(environmentNodeList, nodeId):

    """_summary_
        Findes node by id
    Args:
        environmentNodeList (list): List of node objects
        nodeId (int): Id of node object

    Returns:
        foundNode (object): Node object with Id
    """

    foundNode = None

    for node in environmentNodeList:
        if node.nodeObjectId == nodeId:
            foundNode = node

    return foundNode


def calculate_edge_control_points(environmentEdgeList, smoothingFactor):
    """_summary_
        Calculates control points along each edge
    Args:
        environmentEdgeList (list): List of all edge objects
        smoothingFactor (int): Variable that manages the number of control points
    """

    for edge in environmentEdgeList:
        startPoint, endPoint = edge.start.position, edge.end.position

        controlPoints = list(zip(
            linspace(startPoint[0], endPoint[0], smoothingFactor + 2),
            linspace(startPoint[1], endPoint[1], smoothingFactor + 2)))
        controlPoints.pop(0)
        controlPoints.pop()
        edge.edgeControlPointsList = [list(item) for item in controlPoints]


def find_edge_between_nodes(environmentEdgeList, startNode, endNode):
    """_summary_

    Args:
        environmentEdgeList (list): List of edge object in network
        startNode (object): Start node object of edge
        endNode (object): End node object of edge

    Returns:
        foundEdge (object): Edge object between start and end node
    """

    foundEdge = None

    for edge in environmentEdgeList:
        if edge.start == startNode and edge.end == endNode or edge.start == endNode and edge.end == startNode:
            foundEdge = edge

    return foundEdge
