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

import pandas as pd
pd.set_option("display.max_rows", 4)
pd.set_option("display.max_columns", 6)

# ## Introduction
#
# ## Spatial operations on vector data {#spatial-vec}
#
# ### Spatial subsetting

import geopandas as gpd

# Sample data...

nz = gpd.read_file("data/nz.gpkg")
nz_height = gpd.read_file("data/nz_height.gpkg")

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
