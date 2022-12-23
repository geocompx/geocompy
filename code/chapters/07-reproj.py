# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Reprojecting geographic data {#sec-reproj-geo-data}
#
# ## Prerequisites

#| echo: false
import pandas as pd
import matplotlib.pyplot as plt
pd.options.display.max_rows = 6
pd.options.display.max_columns = 6
pd.options.display.max_colwidth = 35
plt.rcParams['figure.figsize'] = (5, 5)

# Let's import the required packages:

import numpy as np
import geopandas as gpd
import rasterio
import rasterio.warp
from rasterio.plot import show

# and load the sample data:

src_srtm = rasterio.open('data/srtm.tif')
src_nlcd = rasterio.open('data/nlcd.tif')
zion = gpd.read_file('data/zion.gpkg')
world = gpd.read_file('data/world.gpkg')

# ## Introduction
#
# ## Coordinate Reference Systems
#
# ## Querying and setting coordinate systems
#
# Let's look at how CRSs are stored in Python spatial objects and how they can be queried and set. First we will look at getting and setting CRSs in vector geographic data objects. Consider the `GeoDataFrame` object named `world`, imported from a file `world.gpkg`. The object `world` represents countries worldwide. Its CRS can be retrieved using the `.crs` property:

world.crs

# ...
#
# ## Geometry operations on projected and unprojected data {#sec-geometry-operations-on-projected-and-unprojected-data}
#
# ## When to reproject?
#
# ## Which CRS to use?
#
# ## Reprojecting vector geometries {#sec-reprojecting-vector-geometries}
#
# @sec-spatial-class demonstrated how vector geometries are made-up of points, and how points form the basis of more complex objects such as lines and polygons. Reprojecting vectors thus consists of transforming the coordinates of these points, which form the vertices of lines and polygons.
#
# @sec-geometry-operations-on-projected-and-unprojected-data contains an example in which at least one `GeoDataFrame` object must be transformed into an equivalent object with a different CRS to calculate the distance between two objects (?).
#
# ...
#
# ## Reprojecting raster geometries {#sec-reprojecting-raster-geometries}
#
# The projection concepts described in the previous section apply equally to rasters. 
# However, there are important differences in reprojection of vectors and rasters: transforming a vector object involves changing the coordinates of every vertex but this does not apply to raster data. 
# Rasters are composed of rectangular cells of the same size (expressed by map units, such as degrees or meters), so it is usually impracticable to transform coordinates of pixels separately. 
# Raster reprojection involves creating a new raster object, often with a different number of columns and rows than the original. 
# The attributes must subsequently be re-estimated, allowing the new pixels to be 'filled' with appropriate values. 
# In other words, raster reprojection can be thought of as two separate spatial operations: a vector reprojection of the raster extent to another CRS (@sec-reprojecting-vector-geometries), and computation of new pixel values through resampling (@sec-raster-resampling). 
# Thus in most cases when both raster and vector data are used, it is better to avoid reprojecting rasters and reproject vectors instead.
#
# :::{.callout-note}
# Reprojection of the regular rasters is also known as warping. Additionally, there is a second similar operation called "transformation". Instead of resampling all of the values, it leaves all values intact but recomputes new coordinates for every raster cell, changing the grid geometry. For example, it could convert the input raster (a regular grid) into a curvilinear grid. The `rasterio`, like common raster file formats (such as GeoTIFF), does not support curvilinear grids (?).
# :::
#
# The raster reprojection process is done using two functions from the `rasterio.warp` sub-package:
#
# * `rasterio.warp.calculate_default_transform`
# * `rasterio.warp.reproject`
#
# The first function, `calculate_default_transform`, is used to calculate the new transformation matrix in the destination CRS, according to the source raster dimensions and bounds. 
# Alternatively, the destination transformation matrix can be obtained from an existing raster; this is common practice when we need to align one raster with another, for instance to be able to combine them in raster algebra operations (@sec-raster-local-operations) (see below). 
# The second function `rasterio.warp.reproject` then actually calculates cell values in the destination grid, using the user-selected resampling method (such as nearest neighbor, or bilinear). 
#
# Let's take a look at two examples of raster transformation: using categorical and continuous data. 
# Land cover data are usually represented by categorical maps. The `nlcd.tif` file provides information for a small area in Utah, USA obtained from National Land Cover Database 2011 in the NAD83 / UTM zone 12N CRS, as shown in the output of the code chunk below (only first line of output shown). 
# We already created a connection to the `nlcd.tif` file, named `src_nlcd`:

src_nlcd

# Recall that the raster transformation matrix and dimensions are accessible from the file connection as follows. This information will be required to calculate the destination transformation matrix (hereby printed collectively in a `tuple`):

src_nlcd.transform, src_nlcd.width, src_nlcd.height

# First, let's define the destination CRS. In this case, we choose WGS84 (EPSG code `4326`):

dst_crs = 'EPSG:4326'

# Now, we are ready to claculate the destination raster transformation matrix (`dst_transform`), and the destination dimensions (`dst_width`, `dst_height`), as follows: 

dst_transform, dst_width, dst_height = rasterio.warp.calculate_default_transform(
    src_nlcd.crs,
    dst_crs,
    src_nlcd.width,
    src_nlcd.height,
    *src_nlcd.bounds
)
dst_transform, dst_width, dst_height

# Note that `*`, in `*src_nlcd.bounds`, is used to unpack `src_nlcd.bounds` to four separate arguments, which `calculate_default_transform` requires:

src_nlcd.bounds

# Next, we will create the metadata file used for writing the reprojected raster to file. For convenience, we are taking the metadata of the source raster (`src_nlcd.meta`), making a copy (`dst_kwargs`), and then updating those specific properties that need to be changed. Note that the reprojection process typically creates "No Data" pixels, even when there were none in the input raster, since the raster orientation changes and the edges need to be "filled" to get back a rectangular extent. We need to specify a "No Data" value of our choice, if there is none, or use the existing source raster setting, such as `255` in this case:

dst_kwargs = src_nlcd.meta.copy()
dst_kwargs.update({
    'crs': dst_crs,
    'transform': dst_transform,
    'width': dst_width,
    'height': dst_height
})
dst_kwargs

# We are ready to create the reprojected raster. Here, reprojection takes place between two file connections, meaning that the raster value arrays are not being read into memory at once. It is also possible to reproject into an in-memory `ndarray` object, see the [documentation](https://rasterio.readthedocs.io/en/latest/api/rasterio.warp.html#rasterio.warp.reproject).
#
# To write the reprojected raster, we first create a destination file connection `dst_nlcd`, pointing at the output file path of our choice (`output/nlcd_4326.tif`), using the updated metadata object created earlier (`dst_kwargs`):

dst_nlcd = rasterio.open('output/nlcd_4326.tif', 'w', **dst_kwargs)

# Then, we use the `rasterio.warp.reproject` function to calculate and write the reprojection result into the `dst_nlcd` file connection. Note that the `source` and `destination` accept a "band" object, created using `rasterio.band`. In this case, there is just one band. If there were more bands, we would have to repeat the procedure for each band, using `i` instead of `1` inside a [loop](https://rasterio.readthedocs.io/en/latest/topics/reproject.html#reprojecting-a-geotiff-dataset):

rasterio.warp.reproject(
    source=rasterio.band(src_nlcd, 1),
    destination=rasterio.band(dst_nlcd, 1),
    src_transform=src_nlcd.transform,
    src_crs=src_nlcd.crs,
    dst_transform=dst_transform,
    dst_crs=dst_crs,
    resampling=rasterio.warp.Resampling.nearest
)

# Finally, we close the file connection so that the data are actually written:

dst_nlcd.close()

# Many properties of the new object differ from the previous one, including the number of columns and rows (and therefore number of cells), resolution (transformed from meters into degrees), and extent, as summarized again below (note that the number of categories increases from 8 to 9 because of the addition of NA values, not because a new category has been created — the land cover classes are preserved).

src_nlcd.meta

src_nlcd_4326 = rasterio.open('output/nlcd_4326.tif')
src_nlcd_4326.meta

# Examining the unique raster values tells us that the new raster has the same categories, plus the value `255` representing "No Data":

np.unique(src_nlcd.read(1))

np.unique(src_nlcd_4326.read(1))

# +
#| label: fig-raster-reproject-nlcd
#| fig-cap: Reprojecting a categorical raster using nearest neighbor resampling

fig, axes = plt.subplots(ncols=2, figsize=(9,5))
show(src_nlcd, ax=axes[0], cmap='Set3')
show(src_nlcd_4326, ax=axes[1], cmap='Set3')
axes[0].set_title('Original (EPSG:26912)')
axes[1].set_title('Reprojected (EPSG:4326)');
# -

# In the above example, we automatically calculated an optimal (i.e., most information preserving) destination grid using `rasterio.warp.calculate_default_transform`. 
# This is appropriate when there are no specific requirements for the destination raster spatial properties. 
# Namely, we are not required to otain a specific origin and resolution, but just wish to preserve the raster values as much as possible.
# To do that, `calculate_default_transform` "tries" to keep the extent and resolution of the destination raster as similar as possible to the source. 
# In other situations, however, we need to reproject a raster into a specific "template", so that it corresponds, for instance, with other rasters we use in the analysis. 
# In the following code section, we reproject the `nlcd.tif` raster, again, buit this time using the `nlcd_4326.tif` reprojection result as the "template" to demonstrate this alternative workflow.
#
# First, we create a connection to our "template" raster to read its metadata:

template = rasterio.open('output/nlcd_4326.tif')
template.meta

# Then, we create a write-mode connection to our destination raster, using this metadata, meaning that as the resampling result is going to have identical metadata as the "template":

dst_nlcd_2 = rasterio.open('output/nlcd_4326_2.tif', 'w', **template.meta)

# Now, we can resample and write the result:

rasterio.warp.reproject(
    source=rasterio.band(src_nlcd, 1),
    destination=rasterio.band(dst_nlcd_2, 1),
    src_transform=src_nlcd.transform,
    src_crs=src_nlcd.crs,
    dst_transform=dst_nlcd_2.transform,
    dst_crs=dst_nlcd_2.crs,
    resampling=rasterio.warp.Resampling.nearest
)

dst_nlcd_2.close()

# Naturally, in this case, the outputs `nlcd_4326.tif` and `nlcd_4326_2.tif` are identical, as we used the same "template" and the same source data: 

d = rasterio.open('output/nlcd_4326.tif').read(1) == rasterio.open('output/nlcd_4326_2.tif').read(1)
d

np.all(d)

# The difference is that in the first example we calculate the template automatically, using `rasterio.warp.calculate_default_transform`, while in the second example we used an existing raster as the "template".
#
# Importantly, when the template raster has much more "coarse" resolution than the source raster, the:
#
# * `rasterio.warp.Resampling.average` (for continuous rasters), or 
# * `rasterio.warp.Resampling.mode` (for categorical rasters)
#
# resampling method should be used, instead of `rasterio.warp.Resampling.nearest`. Otherwise, much of the data will be lost, as the "nearest" method can capture one pixel value only for each destination raster pixel. 
#
# Reprojecting continuous rasters (with numeric or, in this case, integer values) follows an almost identical procedure. This is demonstrated below with `srtm.tif` from the Shuttle Radar Topography Mission (SRTM), which represents height in meters above sea level (elevation) with the WGS84 CRS.
#
# We will reproject this dataset into a projected CRS, but not with the nearest neighbor method which is appropriate for categorical data. Instead, we will use the bilinear method which computes the output cell value based on the four nearest cells in the original raster. The values in the projected dataset are the distance-weighted average of the values from these four cells: the closer the input cell is to the center of the output cell, the greater its weight. The following code section create a text string representing WGS 84 / UTM zone 12N, and reproject the raster into this CRS, using the bilinear method. The code is practically the same, except for changing the source and destination file names, and replacing `nearest` with `bilinear`:

dst_crs = 'EPSG:32612'
dst_transform, dst_width, dst_height = rasterio.warp.calculate_default_transform(
    src_srtm.crs,
    dst_crs,
    src_srtm.width,
    src_srtm.height,
    *src_srtm.bounds
)
dst_kwargs = src_srtm.meta.copy()
dst_kwargs.update({
    'crs': dst_crs,
    'transform': dst_transform,
    'width': dst_width,
    'height': dst_height
})
dst_srtm = rasterio.open('output/srtm_32612.tif', 'w', **dst_kwargs)
rasterio.warp.reproject(
    source=rasterio.band(src_srtm, 1),
    destination=rasterio.band(dst_srtm, 1),
    src_transform=src_srtm.transform,
    src_crs=src_srtm.crs,
    dst_transform=dst_transform,
    dst_crs=dst_crs,
    resampling=rasterio.warp.Resampling.bilinear
)
dst_srtm.close()

# @fig-raster-reproject-srtm shows the input and the reprojected SRTM rasters.

# +
#| label: fig-raster-reproject-srtm
#| fig-cap: Reprojecting a continuous raster using bilinear resampling

fig, axes = plt.subplots(ncols=2, figsize=(9,5))
show(src_srtm, ax=axes[0])
show(rasterio.open('output/srtm_32612.tif'), ax=axes[1])
axes[0].set_title('Original (EPSG:4326)')
axes[1].set_title('Reprojected (EPSG:32612)');
# -

# ## Custom map projections
#
# ## Exercises
#
