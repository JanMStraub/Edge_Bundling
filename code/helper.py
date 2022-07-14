# -*- coding: utf-8 -*-

# Imports
import json

def readGraphData(path):
    
    # read graph data from JSON
    file = open(path)
    data = json.load(file)
    file.close()
    
    # Read relevant data
    numberOfNodes = data["graph"]["nodesNumber"]
    numberOfEdges = data["graph"]["edgesNumber"]
    edges = data["graph"]["edges"]
    nodes = data["graph"]["properties"]["viewLayout"]["nodesValues"]
    
    nodeList = []
    
    # Convert node to tupel
    for i in range(0, len(nodes)):
        nodeList.append(tuple(map(int, nodes[str(i)].strip("()").split(','))))
    
    return edges, nodeList, numberOfEdges, numberOfNodes


def calculateEdges(node1, node2):
    
    points = []
    ystep = None
    rev = False
    
    x1, y1, z1 = node1.position
    x2, y2, z2 = node2.position
    issteep = abs(y2 - y1) > abs(x2 - x1)
    
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
        
    deltax = x2 - x1
    deltay = abs(y2 - y1)
    error = int(deltax / 2)
    y = y1
    
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
            
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points