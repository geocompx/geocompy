# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3
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

# +
import geopandas as gpd
import numpy as np
import os
import rasterio
import scipy.ndimage

from rasterio.plot import show
# -

# Let us load the sample data for this chapter:

#| echo: false
from pathlib import Path
data_path = Path("data")
file_path = Path("data/landsat.tif")
if not file_path.exists():
  if not data_path.is_dir():
     os.mkdir(data_path)
  print("Attempting to get the data")
  import requests
  r = requests.get("https://github.com/geocompr/py/releases/download/0.1/landsat.tif")  
  with open(file_path, "wb") as f:
    f.write(r.content)

nz = gpd.read_file("data/nz.gpkg")
nz_height = gpd.read_file("data/nz_height.gpkg")
world = gpd.read_file('data/world.gpkg')
src_elev = rasterio.open("data/elev.tif")
src_multi_rast = rasterio.open("data/landsat.tif")

# ## Introduction
#
# ## Spatial operations on vector data {#spatial-vec}
#
# ### Spatial subsetting
#
# Spatial subsetting is the process of taking a spatial object and returning a new object containing only features that relate in space to another object. Analogous to attribute subsetting (covered in @sec-vector-attribute-subsetting), subsets of sf data frames can be created with square bracket ([) operator using the syntax x[y, , op = st_intersects], where x is an sf object from which a subset of rows will be returned, y is the ‘subsetting object’ and , op = st_intersects is an optional argument that specifies the topological relation (also known as the binary predicate) used to do the subsetting. The default topological relation used when an op argument is not provided is st_intersects(): the command x[y, ] is identical to x[y, , op = st_intersects] shown above but not x[y, , op = st_disjoint] (the meaning of these and other topological relations is described in the next section). The filter() function from the tidyverse can also be used but this approach is more verbose, as we will see in the examples below.
#
# To demonstrate spatial subsetting, we will use the nz and nz_height datasets in the spData package, which contain geographic data on the 16 main regions and 101 highest points in New Zealand, respectively (@fig-spatial-subset), in a projected coordinate system. The following code chunk creates an object representing Canterbury, then uses spatial subsetting to return all high points in the region:

canterbury = nz[nz["Name"] == "Canterbury"]
sel = nz_height.intersects(canterbury['geometry'].iloc[0])
canterbury_height = nz_height[sel]

# +
#| label: fig-spatial-subset
#| fig-cap: Spatial subsetting of points by intersection with polygon

fig, axes = plt.subplots(1, 2, figsize=(8, 4))
base = nz.plot(color="white", edgecolor="lightgrey", ax=axes[0])
nz_height.plot(ax=base, color="None", edgecolor="red")
base = nz.plot(color="white", edgecolor="lightgrey", ax=axes[1])
canterbury_height.plot(ax=base, color="None", edgecolor="red");
# -

# Spatial subsetting 2...

non_canterbury_height = nz_height.overlay(canterbury, how='difference')

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

# +
from shapely.geometry import Point, LineString, Polygon
points = gpd.GeoSeries([Point(0.2,0.1), Point(0.7,0.2), Point(0.4,0.8)])
line = LineString([(0.4,0.2), (1,0.5)])
poly = Polygon([(0,0), (0,1), (1,1), (1,0.5), (0,0)])

p = gpd.GeoSeries(poly).plot(color='yellow')
p = gpd.GeoSeries(line).plot(ax=p, color='red')
points.plot(ax=p)
# -

points.intersects(poly)

points.within(poly)

points.touches(poly)

points.disjoint(poly)

points.distance(poly) < 0.2

# ### DE-9IM strings
#
# ...
#
#
#
# ### Spatial joining
#
# Joining two non-spatial datasets relies on a shared 'key' variable, as described in @sec-vector-attribute-joining. Spatial data joining applies the same concept, but instead relies on spatial relations, described in the previous section. As with attribute data, joining adds new columns to the target object (the argument x in joining functions), from a source object (y).
#
# The process is illustrated by the following example: imagine you have ten points randomly distributed across the Earth's surface and you ask, for the points that are on land, which countries are they in? Implementing this idea in a reproducible example will build your geographic data handling skills and show how spatial joins work. The starting point is to create points that are randomly scattered over the Earth's surface:

np.random.seed(11)  ## set seed for reproducibility
bb = world.total_bounds  ## the world's bounds
x = np.random.uniform(low=bb[0], high=bb[2], size=10)
y = np.random.uniform(low=bb[1], high=bb[3], size=10)
random_points = gpd.points_from_xy(x, y, crs=4326)
random_points = gpd.GeoSeries(random_points)
random_points = gpd.GeoDataFrame({'geometry': random_points})
random_points

# The scenario illustrated in @fig-spatial-join shows that the `random_points` object (top left) lacks attribute data, while the world (top right) has attributes, including country names shown for a sample of countries in the legend. Spatial joins are implemented with `gpd.sjoin`, as illustrated in the code chunk below. The output is the `random_joined` object which is illustrated in @fig-spatial-join (bottom left). Before creating the joined dataset, we use spatial subsetting to create world_random, which contains only countries that contain random points, to verify the number of country names returned in the joined dataset should be four (see the top right panel of @fig-spatial-join).

# Subset
world_random = world[world.intersects(random_points.unary_union)]
world_random

# Spatial join
random_joined = gpd.sjoin(random_points, world, how='left')
random_joined

# +
#| label: fig-spatial-join
#| fig-cap: >-
#|   Illustration of a spatial join. A new attribute variable is added to random
#|   points (top left) from source world object (top right) resulting in the data
#|   represented in the final panel.

fig, axes = plt.subplots(2, 2, figsize=(9, 5))
base = world.plot(color="white", edgecolor="lightgrey", ax=axes[0][0])
random_points.plot(ax=base, color="None", edgecolor="red")
base = world.plot(color="white", edgecolor="lightgrey", ax=axes[0][1])
world_random.plot(ax=base, column='name_long')
base = world.plot(color="white", edgecolor="lightgrey", ax=axes[1][0])
random_joined.geometry.plot(ax=base, color='grey');
random_joined.plot(ax=base, column='name_long', legend=True);
# -

# ### Non-overlapping joins
#
# ...
#
#
#
#
# ### Spatial aggregation
#
# ...
#
#
#
# ### Joining incongruent layers
#
# ...
#
#
#
# ### Distance relations
#
# ...
#
#
#
#
# ## Spatial operations on raster data {#spatial-ras}
#
# ### Spatial subsetting
#
# The previous chapter (Section ...) demonstrated how to retrieve values associated with specific cell IDs or row and column combinations. Raster objects can also be extracted by location (coordinates) and other spatial objects. To use coordinates for subsetting, we can use the `.sample` method of a `rasterio` file connection object, combined with a list of coordinate tuples. The methods is demonstrated below to find the value of the cell that covers a point located at coordinates of 0.1, 0.1 in `elev`. The resutned object is a *generator*; in case we want all values at once we can apply `list`. The result is `16`:

list(src_elev.sample([(0.1, 0.1)]))

# Raster objects can also be subset with another raster object, as demonstrated in the code chunk below:
#
# ...

# +
# ...
# -

# Another common use case of spatial subsetting is using a boolean mask, based on another raster with the same extent and resolution, or the original one, as illustrated in Figure .... To do that, we "erase" the values in the array of one raster, according to another corresponding "mask" raster. For example, let us read the `elev.tif` raster array: 

elev = src_elev.read(1)
elev

# and create a correspinding random mask:

np.random.seed(1)
mask = np.random.choice([True, False], elev.shape)
mask

# In the code chunk above, we have created a mask object called `mask` with values randomly assigned to `True` and `False`. Next, we want to keep those values of `elev` which are `False` in `mask` (i.e., they are *not* masked). In other words, we want to mask `elev` with `mask`. The result is stored in a copy named `elev1`:

elev1 = elev.copy()
elev1[mask] = np.nan
elev1

# The result is shown in figure...

fig, axes = plt.subplots(ncols=3, figsize=(9,5))
show(elev, ax=axes[0])
show(mask, ax=axes[1])
show(elev1, ax=axes[2])
axes[0].set_title("Original")
axes[1].set_title("Mask")
axes[2].set_title("Result");

# The above approach can be also used to replace some values (e.g., expected to be wrong) with `nan`:

elev[elev < 20] = np.nan
elev

# These operations are in fact Boolean local operations, since we compare cell-wise two rasters. The next subsection explores these and related operations in more detail.
#
# ### Map algebra
#
# The term ‘map algebra’ was coined in the late 1970s to describe a “set of conventions, capabilities, and techniques” for the analysis of geographic raster and (although less prominently) vector data (Tomlin 1994). In this context, we define map algebra more narrowly, as operations that modify or summarise raster cell values, with reference to surrounding cells, zones, or statistical functions that apply to every cell.
#
# Map algebra operations tend to be fast, because raster datasets only implicitly store coordinates, hence the old adage “raster is faster but vector is corrector”. The location of cells in raster datasets can be calculated by using its matrix position and the resolution and origin of the dataset (stored in the header). For the processing, however, the geographic position of a cell is barely relevant as long as we make sure that the cell position is still the same after the processing. Additionally, if two or more raster datasets share the same extent, projection and resolution, one could treat them as matrices for the processing.
#
# This is the way that map algebra works with the terra package. First, the headers of the raster datasets are queried and (in cases where map algebra operations work on more than one dataset) checked to ensure the datasets are compatible. Second, map algebra retains the so-called one-to-one locational correspondence, meaning that cells cannot move. This differs from matrix algebra, in which values change position, for example when multiplying or dividing matrices.
#
# Map algebra (or cartographic modeling with raster data) divides raster operations into four subclasses (Tomlin 1990), with each working on one or several grids simultaneously:
#
# * Local or per-cell operations
# * Focal or neighborhood operations. Most often the output cell value is the result of a 3 x 3 input cell block
# * Zonal operations are similar to focal operations, but the surrounding pixel grid on which new values are computed can have irregular sizes and shapes
# * Global or per-raster operations; that means the output cell derives its value potentially from one or several entire rasters
#
# This typology classifies map algebra operations by the number of cells used for each pixel processing step and the type of the output. For the sake of completeness, we should mention that raster operations can also be classified by discipline such as terrain, hydrological analysis, or image classification. The following sections explain how each type of map algebra operations can be used, with reference to worked examples.
#
#
# ### Local operations
#
#
# First, we need to read raster values:

elev = src_elev.read(1)
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
# $$NDVI=\frac{NIR-Red} {NIR+Red}$$
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
# While local functions operate on one cell, though possibly from multiple layers, focal operations take into account a central (focal) cell and its neighbors. The neighborhood (also named kernel, filter or moving window) under consideration is typically of size 3-by-3 cells (that is the central cell and its eight surrounding neighbors), but can take on any other (not necessarily rectangular) shape as defined by the user. A focal operation applies an aggregation function to all cells within the specified neighborhood, uses the corresponding output as the new value for the the central cell, and moves on to the next central cell (Figure ...). Other names for this operation are spatial filtering and convolution (Burrough, McDonnell, and Lloyd 2015).
#
# In Python, the `scipy.ndimage` package has a comprehensive collection of [functions](https://docs.scipy.org/doc/scipy/reference/ndimage.html#filters) to perform filtering of `numpy` arrays, such as:
#
# * `minimum_filter`
# * `maximum_filter`
# * `uniform_filter` (i.e., mean filter)
# * `median_filter`
# etc.
#
# In this group of functions, we define the shape of the moving window with either one of:
#
# * `size`—a single number or tuple, implying a filter of those dimensions
# * `footprint`—a boolean array, representing both the window shape and the identity of elements being included
#
# In addition to specific built-in filters, 
#
# * `convolve` applies the sum function after multiplying by a custom `weights` array
# * `generic_filter` makes it possible to pass any custom function, where the user can specify any type of custom window-based calculatio.
#
# For example, here we apply the minimum filter with window size of `3` on `elev`: 

elev

elev_min = scipy.ndimage.minimum_filter(elev, size=3)
elev_min

# Special care should be given to the edge pixels. How should they be calculated? `scipy.ndimage` gives several options through the `mode` parameter:
#
# * `reflect` (the default)
# * `constant`
# * `nearest`
# * `mirror`
# * `wrap`
#
# Sometimes artificially extending raster edges is considered unsuitable. In other words, we may wish the resulting raster to contain pixel values with "complete" windows only, for example to have a uniform sample size or because values in all directions matter (such as in topographic calculations). There is no specific option *not* to extent edges in `scipy.ndimage`. However, to get the same effect, the edges of the filtered array can be assigned with `nan`, in a number of rows and columns according to filter size. For example, when using a filter of `size=3`, the first "layer" of pixels may be assigned with `nan`, reflecting the fact that these pixels have incomplete 3*3 neighborhoods:

elev_min[:, [0, -1]] = np.nan
elev_min[[0, -1], :] = np.nan
elev_min

# We can quickly check if the output meets our expectations. In our example, the minimum value has to be always the upper left corner of the moving window (remember we have created the input raster by row-wise incrementing the cell values by one starting at the upper left corner). 
#
# Focal functions or filters play a dominant role in image processing. Low-pass or smoothing filters use the mean function to remove extremes. In the case of categorical data, we can replace the mean with the mode, which is the most common value. By contrast, high-pass filters accentuate features. The line detection Laplace and Sobel filters might serve as an example here. 
#
# Terrain processing, the calculation of topographic characteristics such as slope, aspect and flow directions, relies on focal functions. The `TerrainAttribute` function from package `richdem` can be used to calculate common [metrics](https://richdem.readthedocs.io/en/latest/python_api.html?highlight=TerrainAttribute#richdem.TerrainAttribute), specified through the `attrib` argument, namely:
#
# * `slope_riserun` 	Horn (1981) doi: 10.1109/PROC.1981.11918
# * `slope_percentage` 	Horn (1981) doi: 10.1109/PROC.1981.11918
# * `slope_degrees` 	Horn (1981) doi: 10.1109/PROC.1981.11918
# * `slope_radians` 	Horn (1981) doi: 10.1109/PROC.1981.11918
# * `aspect` 	Horn (1981) doi: 10.1109/PROC.1981.11918
# * `curvature` 	Zevenbergen and Thorne (1987) doi: 10.1002/esp.3290120107
# * `planform_curvature` 	Zevenbergen and Thorne (1987) doi: 10.1002/esp.3290120107
# * `profile_curvature` 	Zevenbergen and Thorne (1987) doi: 10.1002/esp.3290120107
#
#
#
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
#
# * Write a function which accepts and array and an `int` specifying the number of rows/columns to erase along an array edges. The function needs to return the modified array with `nan` values along its edges.
#
