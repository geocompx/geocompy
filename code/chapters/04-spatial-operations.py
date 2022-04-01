# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Spatial data operations {#spatial-operations}
#
# ## Prerequisites

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

nz = gpd.read_file("data/nz.gpkg")
nz_height = gpd.read_file("data/nz_height.gpkg")
src_elev = rasterio.open("data/elev.tif")
# src_multi_rast = rasterio.open("data/landsat.tif")

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
# ...
#
# ### Focal operations
#
# For focal operations, we first need to read raster values:

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
axes[0].set_title("elev+elev", cmap="Oranges")
axes[1].set_title("elev ** 2", cmap="Oranges")
axes[2].set_title("np.log(elev)", cmap="Oranges")
axes[3].set_title("elev > 5", cmap="Oranges");

# Example of reclassify...
#
# Here, we assign the raster values in the ranges 0–12, 12–24 and 24–36 are reclassified to take values 1, 2 and 3, respectively...

# NDVI...

# +
# multi_rast = src_multi_rast.read()
# nir = multi_rast[3,:,:]
# red = multi_rast[2,:,:]
# ndvi = (nir-red)/(nir+red)
# -

# Convert values >1 to "No Data":

# +
# ndvi[ndvi>1] = np.nan
# -

# Plot...

# +
# fig, axes = plt.subplots(ncols=2, figsize=(9,5))
# show(multi_rast[(2,1,0), :, :]/multi_rast.max(), ax=axes[0], cmap="RdYlGn")
# show(ndvi, ax=axes[1], cmap="Greens")
# -

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
