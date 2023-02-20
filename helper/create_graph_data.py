# -*- coding: utf-8 -*-

"""
This algorithm is used to create random graph data
@author: Jan Straub
"""

# Imports
import random


def random_graph():
    numberOfNodes = 10
    numberOfEdges = 30
    size = 10

    nodeList = random_nodes(numberOfNodes, size)
    random_edges(numberOfNodes, numberOfEdges, nodeList)


def random_nodes(numberOfNodes, size):
    nodeList = []
    id = 0
    while id < numberOfNodes:
        x = random.randrange(0, size)
        y = random.randrange(0, size)
        if [x, y] not in nodeList and [y, x] not in nodeList:
            nodeList.append([x, y])
            print(f"\"{id}\": \"({x},{y},0)\",")
            id += 1

    return nodeList


def random_edges(numberOfNodes, numberOfEdges, nodeList):
    edgeList, edgeStartList, edgeEndList = [], [], []
    iterator = 0
    
    while iterator < numberOfEdges:
        start = random.randrange(0, numberOfNodes)
        end = random.randrange(0, numberOfNodes)
        if start != end:
            if [start, end] not in edgeList and [end, start] not in edgeList:
                edgeList.append([start, end])
                edgeStartList.append(start)
                edgeEndList.append(end)
                print(f"[{start}, {end}],")
                iterator += 1

    for i in range(0, len(nodeList)):
        if i in edgeStartList or i in edgeEndList:
            continue
        else:
            raise ValueError("Not all nodes have edges")

    
if __name__ == "__main__":

    random_graph()