# -*- coding: utf-8 -*-

"""
This file calculates the quality metrics of graph bundles
@author: Jan Straub
"""

# Imports
from json import load
from PIL import Image
from helper import calculate_distance_between_positions, read_graph_data

def get_black_white_image(path):
    """_summary_
        Function calculates black pixel count
    Args:
        path (string): The path where the code is based
    """

    im = Image.open(path)

    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    numberOfPixels = 0
    numberOfNonWhitePixels = 0

    for x in pixels:
        for y in x:
            R = y[0]
            G = y[1]
            B = y[2]
            numberOfPixels += 1
            if R != 255 and G != 255 and B != 255:
                numberOfNonWhitePixels += 1

    print(f"Non white pixel: {numberOfNonWhitePixels} from {numberOfPixels}")


def get_distortion_value(jsonFilePath):
    """_summary_
        Function calculates the distortion value of a graph
    Args:
        jsonFilePath (string): Path to json file
    """
    nodeList, pathList = read_graph_data(jsonFilePath)
    originalDistance = 0

    for path in pathList:
        start = []
        end = []

        for index, node in enumerate(nodeList):

            if path[0] == index:
                start = node
            if path[1] == index:
                end = node

        originalDistance += calculate_distance_between_positions(start, end)

    print(f"Original distance: {originalDistance}")


def get_distortion_value_wr(jsonFilePath):
    """_summary_
        Function calculates the distortion value of a Winding Roads graph
    Args:
        jsonFilePath (string): Path to json file
    """

    # read graph data from JSON
    with open(jsonFilePath, mode = "r", encoding = "utf-8") as file:
        data = load(file)

    # Read relevant data
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
    edges = data["graph"]["properties"]["viewLayout"]["edgesValues"]
    pathList = data["graph"]["edges"]

    nodeList = []
    edgeList = []
    nodeListAppend = nodeList.append
    edgeListAppend = edgeList.append

    # Convert node to tupel
    for i in range(len(nodes)):
        nodePosition = tuple(map(float, nodes[str(i)].strip("()").split(",")))
        nodeListAppend(nodePosition[:2])

    # Convert edge to tupel
    for key, values in edges.items():
        pathPositions = []
        edgePosition = tuple(map(str, values.strip("()").split(",0)")))
        for point in edgePosition:
            newPoint = point.strip(",0")
            pointPosition = tuple(map(float, newPoint.strip(", (").split(",")))
            pathPositions.append(pointPosition)
        edgeListAppend(pathPositions)

    originalDistance = 0

    for pathIndex, path in enumerate(pathList):
        start = 0
        end = 0

        for nodeIndex, node in enumerate(nodeList):

            if path[0] == nodeIndex:
                start = node
            if path[1] == nodeIndex:
                end = node
        oldPoint = None
        for position, bezierPoint in enumerate(edgeList[pathIndex]):

            if position == 0:
                originalDistance += calculate_distance_between_positions(start, bezierPoint)
                oldPoint = bezierPoint
            elif position == len(edgeList[pathIndex]):
                originalDistance += calculate_distance_between_positions(end, bezierPoint)
            else:
                originalDistance += calculate_distance_between_positions(oldPoint, bezierPoint)
                oldPoint = bezierPoint

        #originalDistance += calculate_distance_between_positions(start, end)

    print(f"Winding roads distance: {originalDistance}")


if __name__ == "__main__":

    # Setup parameter
    IMAGE_PATH = "/Users/jan/Documents/code/gitlab_BA/2023-jan-straub/plots/compare/10x10_10n_30e/"
    IMAGE_NAME = "10x10_10n_30e_12-1000"
    IMAGE_FILE_PATH = IMAGE_PATH + IMAGE_NAME + ".png"

    get_black_white_image(IMAGE_FILE_PATH)

    JSON_PATH = "/Users/jan/Documents/code/gitlab_BA/2023-jan-straub"
    JSON_FILE_NAME = "10x10_10n_30e"
    JSON_FILE_PATH = JSON_PATH + "/data/" + JSON_FILE_NAME + ".json"

    #get_distortion_value(JSON_FILE_PATH)

    JSON_PATH = "/Users/jan/Documents/code/gitlab_BA/2023-jan-straub/"
    JSON_FILE_NAME = "wr_10x10_10n_30e_graph"
    JSON_FILE_PATH = JSON_PATH + "/data/" + JSON_FILE_NAME + ".json"

    #get_distortion_value_wr(JSON_FILE_PATH)
