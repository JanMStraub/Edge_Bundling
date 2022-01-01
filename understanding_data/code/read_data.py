

from scipy.io import netcdf
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import pyvista as pv


file2read = netcdf.NetCDFFile('/Users/jan/Google Drive/Programmieren/bachelor_thesis/understanding_data/data/adaptor.mars.internal-1638955599.573768-27854-3-4f5a652e-900a-48d1-a6ad-8fd1fadf9d88.nc','r')


longitude = file2read.variables["longitude"][:100].copy()
latitude = file2read.variables["latitude"][:100].copy()
level = file2read.variables["level"][:100].copy()
time = file2read.variables["time"][:100].copy()
t = file2read.variables["t"][:1].copy()
u = file2read.variables["u"][:1].copy()
v = file2read.variables["v"][:1].copy()
w = file2read.variables["w"][:1].copy()

grid = pv.UniformGrid()

grid.dimensions = 

file2read.close()


 