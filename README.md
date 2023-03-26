# PROJECT DESCRIPTION

[Title] Local Iterative Optimization for Graph Bundling

[Short abstract]
_In this thesis, we presented a novel edge bundling technique based on a Physarium approximation of a Steiner tree. This Steiner tree is then used as a routing structure for graph paths. The resulting drawings consist of densely bundled graphs that reduce node-edge overlaps and make it easier to get an overview of the graph data._

[Type of Project] Bachelor thesis

- Project start date: 20.10.2022
- Project due date: 20.02.2022

<details><summary>Supervisors</summary>

- Project Owner: Jan Straub
- Supervisor: Filip Sadlo
- Assistant: Maksim Schreck

</details>

## Status

- [x] Registrated (20.10.2022)
- [x] Work submitted (20.02.2023)
- [x] Final presentation done (13.03.2023) 
- [x] Uploaded all materials (13.03.2023) 

# Installation

This guide only applies to MacOS.

Make sure to have python installed and to download all required packages first, i.e. run:
```
pip install -r requirements.txt
```

# Usage

WARNING: Change the PATH (below) before running the code.
If you just want to test if everyting works correctly navigate to the _code_ folder and run:
```
python3 main.py
```
In the folder _plots_ should new be a new file with the default test graph.

## Data
In the folder _data_ you will find the different JSON graph files we used.

### Create own data
If you want to create your own graph data go in the _helper_ folder.
In the **create_graph_data.py** file you can define the number of nodes, number of edges and the size of the graph.
After that duplicate a JSON file and paste the output in the right place.

### Transfere data
If you want to test the JSON data on other graph bundling approaches (e.g. Edge-Path Bundling) use the **transfer_json.py** file to change the format of the data and paste the output in the right place.

## Parameters
To generate own plots you have to edit the **main.py** file.
At the end of it you find the all parameters that can be changes.

### Path
Change the PATH variable to your path
### JSON_FILE_NAME
Change the JSON_FILE_NAME to the name of the JSON data you want to use
### PLOT_SELECTION
Choose the mode in which the algorithm should run.
  * 0: The algorithm calculates a new graph from the JSON data
  * 1: If you already calculated a graph with the selected JSON data and just want to try a different post processing method, you can use this option. The algorithm selects the saved network from the folder _savedNetworks_
  * 2: Allows you to plot the unbundled graph
### POST_PROCESSING_SELECTION
Choose the look of the result
  * 0: Plot the underlying Steiner tree structure
  * 1: Plot the Bezier curve bundling (default)
  * 2: Plot the cubic spline bundling
### SMOOTHING
Allows you to choose a different smoothing factor. Is unstable for values above 2.
  * 0: Steiner points are the control points
  * 1: The middle of each edge is the control point

# Known issues
  * There is an math error issue that sometimes comes up, just rerun the code.