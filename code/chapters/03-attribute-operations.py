# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: OSMNX
#     language: python
#     name: osmnx
# ---

# # Attribute data operations {#attr}

import pandas as pd
pd.set_option("display.max_rows", 4)
pd.set_option("display.max_columns", 6)

# ## Introduction
#
# ## Vector attribute manipulation
#
# ### Vector attribute subsetting

import geopandas as gpd

world = gpd.read_file("data/world.gpkg")
world

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
# Subsetting by row/column...
#
# ### Summarizing raster objects
#
# Global summary of raster values (mean, etc.)...
#
# Histogram of raster values...
#
# ## Exercises
