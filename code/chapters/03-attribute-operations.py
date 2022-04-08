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

# # Attribute data operations {#attr}
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

# Sample data...

world = gpd.read_file("data/world.gpkg")
src_elev = rasterio.open("data/elev.tif")
src_multi_rast = rasterio.open("data/landsat.tif")

# ## Introduction
#
# ## Vector attribute manipulation
#
# ### Vector attribute subsetting
#
# Subsetting rows by attribute...
#
# Selecting columns...

world[["name_long", "geometry"]]

# ### Vector attribute aggregation
#
# Aggregation without geometry...
#
# ### Vector attribute joining
#
# Join by attribute...

import pandas as pd

coffee_data = pd.read_csv("data/coffee_data.csv")
coffee_data

# Join by `"name_long"` column...

world_coffee = pd.merge(world, coffee_data, on = "name_long", how = "left")
world_coffee

# Plot... 

base = world.plot(color = "white", edgecolor = "lightgrey")
world_coffee.plot(ax = base, column = "coffee_production_2017");

# ### Creating attributes and removing spatial information
#
# Calculate new column...

world2 = world.copy()
world2["pop_dens"] = world2["pop"] / world2["area_km2"]

# Unite columns...

world2["con_reg"] = world["continent"] + ":" + world2["region_un"]
world2 = world2.drop(["continent", "region_un"], axis=1)

# Split column...

world2[["continent", "region_un"]] = world2["con_reg"].str.split(":", expand=True)

# Rename...

world2.rename(columns={"name_long": "name"})

# Renaming all columns...

new_names =["i", "n", "c", "r", "s", "t", "a", "p", "l", "gP", "geom"]
world.columns = new_names

# Dropping geometry...

pd.DataFrame(world.drop(columns="geom"))

# ## Manipulating raster objects
#
# ### Raster subsetting
#
# When using `rasterio`, raster values are accessible through a `numpy` array, which can be imported with the `.read` method:

elev = src_elev.read(1)
elev

# Then, we can access any subset of cell values using `numpy` methods. For example:

elev[0, 0]  ## Value at row 1, column 1

# Cell values can be modified by overwriting existing values in conjunction with a subsetting operation. The following expression, for example, sets the upper left cell of elev to 0:

elev[0, 0] = 0
elev

# Multiple cells can also be modified in this way:

elev[0, 0:2] = 0
elev

# ### Summarizing raster objects
#
# Global summaries of raster values can be calculated by applying `numpy` summary functions---such as `np.mean`---on the array with raster values. For example:
#
# ```{numpy}
# np.mean(elev)
# ```
#
# Note that "No Data"-safe functions--such as `np.nanmean`---should be used in case the raster contains "No Data" values which need to be ignored:
#
# ```{numpy}
# elev[0, 2] = np.nan
# elev
# ```
#
# ```{numpy}
# np.mean(elev)
# ```
#
# ```{numpy}
# np.nanmean(elev)
# ```
#
# Raster value statistics can be visualized in a variety of ways. One approach is to "flatten" the raster values into a one-dimensional array, then use a graphical function such as `plt.hist` or `plt.boxplot` (from `matplotlib.pyplot`). For example:

x = elev.flatten()
plt.hist(x);

# ## Exercises
#
