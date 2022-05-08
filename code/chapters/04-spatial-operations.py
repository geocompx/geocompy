# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Spatial data operations {#spatial-operations}
#
# ## Prerequisites

#| echo: false
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option("display.max_rows", 4)
pd.set_option("display.max_columns", 6)
pd.options.display.max_rows = 10
pd.options.display.max_columns = 6
pd.options.display.max_colwidth = 35
plt.rcParams["figure.figsize"] = (5, 5)

# Packages...

import numpy as np
import geopandas as gpd
import rasterio
from rasterio.plot import show

# Let us load the sample data for this chapter:

#| echo: false
from pathlib import Path
data_path = Path("data")
file_path = Path("data/landsat.tif")
if not file_path.exists():
  if not data_path.is_dir():
     os
     os.mkdir(data_path)
  import os
  print("Attempting to get the data")
  import requests
  r = requests.get("https://github.com/geocompr/py/releases/download/0.1/landsat.tif")  
  with open(file_path, "wb") as f:
    f.write(r.content)

nz = gpd.read_file("data/nz.gpkg")
nz_height = gpd.read_file("data/nz_height.gpkg")
src_elev = rasterio.open("data/elev.tif")
src_multi_rast = rasterio.open("data/landsat.tif")

# ## Introduction
#
# ## Spatial operations on vector data {#spatial-vec}
#
# ### Spatial subsetting
#
# Plot...

base = nz.plot(color="white", edgecolor="lightgrey")
nz_height.plot(ax=base, color="None", edgecolor="red");

# Spatial subsetting...

canterbury = nz[nz["Name"] == "Canterbury"]
sel = nz_height.intersects(canterbury["geometry"].iloc[0])
canterbury_height = nz_height[sel]

# Plot...

base = nz.plot(color="white", edgecolor="lightgrey")
canterbury_height.plot(ax=base, color="None", edgecolor="red");

# Spatial subsetting 2...

sel = nz_height.disjoint(canterbury["geometry"].iloc[0])
non_canterbury_height = nz_height[sel]

# Plot...

base = nz.plot(color="white", edgecolor="lightgrey")
non_canterbury_height.plot(ax=base, color="None", edgecolor="red");

# ...
#
#
#
# ### Topological relations
#
# ...
#
# ### DE-9IM strings
#
# ...
#
# ### Spatial joining
#
# ...
#
# ### Non-overlapping joins
#
# ...
#
# ### Spatial aggregation
#
# ...
#
# ### Joining incongruent layers
#
# ...
#
# ### Distance relations
#
# ...
#
# ## Spatial operations on raster data {#spatial-ras}
#
# ### Spatial subsetting
#
# ...
#
# ### Map algebra
#
# ...
#
# ### Local operations
#
#
# First, we need to read raster values:

elev = src_elev.read()
elev

# Now, any element-wise array operation can be applied. For example:

elev + elev

# Here are few more examples:

fig, axes = plt.subplots(ncols=4, figsize=(9,5))
show(elev + elev, ax=axes[0], cmap="Oranges")
show(elev ** 2, ax=axes[1], cmap="Oranges")
show(np.log(elev), ax=axes[2], cmap="Oranges")
show(elev > 5, ax=axes[3], cmap="Oranges")
axes[0].set_title("elev+elev")
axes[1].set_title("elev ** 2")
axes[2].set_title("np.log(elev)")
axes[3].set_title("elev > 5");

# Another good example of local operations is the classification of intervals of numeric values into groups such as grouping a digital elevation model into low (class 1), middle (class 2) and high elevations (class 3). Here, we assign the raster values in the ranges 0–12, 12–24 and 24–36 are reclassified to take values 1, 2 and 3, respectively...

recl = elev.copy()
recl[(elev > 0)  & (elev <= 12)] = 1
recl[(elev > 12) & (elev <= 24)] = 2
recl[(elev > 24) & (elev <= 36)] = 3

# Plot...

fig, axes = plt.subplots(ncols=2, figsize=(9,5))
show(elev, ax=axes[0], cmap="Oranges")
show(recl, ax=axes[1], cmap="Oranges")
axes[0].set_title("Original")
axes[1].set_title("Reclassified");

# The calculation of the normalized difference vegetation index (NDVI) is a well-known local (pixel-by-pixel) raster operation. It returns a raster with values between -1 and 1; positive values indicate the presence of living plants (mostly > 0.2). NDVI is calculated from red and near-infrared (NIR) bands of remotely sensed imagery, typically from satellite systems such as Landsat or Sentinel. Vegetation absorbs light heavily in the visible light spectrum, and especially in the red channel, while reflecting NIR light, explaining the NVDI formula:
#
# $NDVI=\frac{NIR+Red} {NIR-Red}$
#
# Let's calculate NDVI for the multispectral satellite file of the Zion National Park.

multi_rast = src_multi_rast.read()
nir = multi_rast[3,:,:]
red = multi_rast[2,:,:]
ndvi = (nir-red)/(nir+red)

# Convert values >1 to "No Data":

ndvi[ndvi>1] = np.nan

# When plotting an RGB image using the `show` function, the function assumes that:
#
# * Values are in the range `[0,1]` for floats, or `[0,255]` for integers (otherwise clipped)
# * The order of bands is RGB
#
# To "prepare" the multi-band raster for `show`, we therefore reverse the order of bands (which is originally BGR+NIR), and divided by the maximum to set the maximum value at `1`:

multi_rast_rgb = multi_rast[(2,1,0), :, :]/multi_rast.max()

# Plot...

fig, axes = plt.subplots(ncols=2, figsize=(9,5))
show(multi_rast_rgb, ax=axes[0], cmap="RdYlGn")
show(ndvi, ax=axes[1], cmap="Greens")
axes[0].set_title("RGB image")
axes[1].set_title("NDVI");

# ### Focal operations
#
# ...
#
# ### Zonal operations
#
# ...
#
# ### Global operations and distances
#
# ...
#
# ### Map algebra counterparts in vector processing
#
# ...
#
# ### Merging rasters
#
# ...
#
# ## Exercises