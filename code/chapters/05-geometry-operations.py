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

# # Geometry operations {#geometric-operations}
#
# ## Prerequisites

import pandas as pd
pd.set_option("display.max_rows", 4)
pd.set_option("display.max_columns", 6)

# Packages...

import matplotlib.pyplot as plt
import geopandas as gpd

# Sample data...

seine = gpd.read_file("data/seine.gpkg")

# ## Introduction
#
# ## Geometric operations on vector data {#geo-vec}
#
# ### Simplification
#
# Simplify...

seine_simp = seine.simplify(2000)  # 2000 m

# Plot:

fig, axes = plt.subplots(ncols=2)
seine.plot(ax=axes[0])
seine_simp.plot(ax=axes[1])
axes[0].set_title("Original")
axes[1].set_title("Simplified (d=2000 m)")

# Compare number of nodes:

import sys
sys.getsizeof(seine)       ## Bytes

sys.getsizeof(seine_simp)  ## Bytes

len(list(seine_simp.iloc[0].coords)) # Simplified

# ### Centroids
#
# ...

# ### Buffers
#
# ...

# ### Affine transformations
#
# ...

# ### Clipping
#
# ...

# ### Subsetting and clipping
#
# ...

# ### Geometry unions
#
# ...

# ### Type transformations
#
# ...

# ## Geometric operations on raster data {#geo-ras}
#
# ### Geometric intersections
#
# ...

# ### Extent and origin
#
# ...

# ### Aggregation and disaggregation
#
# ...

# ### Resampling
#
# ...

# ## Exercises
#
