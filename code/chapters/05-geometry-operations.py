# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Geometry operations {#geometric-operations}
#
# ## Prerequisites

#| echo: false
import pandas as pd
import matplotlib.pyplot as plt
pd.options.display.max_rows = 6
pd.options.display.max_columns = 6
pd.options.display.max_colwidth = 35
plt.rcParams["figure.figsize"] = (5, 5)

# Packages...

import shapely.geometry
import geopandas as gpd

# Sample data...

seine = gpd.read_file("data/seine.gpkg")
us_states = gpd.read_file("data/us_states.gpkg")
nz = gpd.read_file("data/nz.gpkg")

# ## Introduction
#
# So far the book has explained the structure of geographic datasets (Chapter 2), and how to manipulate them based on their non-geographic attributes (Chapter 3) and spatial relations (Chapter 4). This chapter focusses on manipulating the geographic elements of geographic objects, for example by simplifying and converting vector geometries, cropping raster datasets, and converting vector objects into rasters and from rasters into vectors. After reading it---and attempting the exercises at the end---you should understand and have control over the geometry column in sf objects and the extent and geographic location of pixels represented in rasters in relation to other geographic objects.
#
# @sec-geo-vec covers transforming vector geometries with 'unary' and 'binary' operations. Unary operations work on a single geometry in isolation, including simplification (of lines and polygons), the creation of buffers and centroids, and shifting/scaling/rotating single geometries using 'affine transformations' (@sec-simplification to @sec-affine-transformations). Binary transformations modify one geometry based on the shape of another, including clipping and geometry unions, covered in @sec-clipping and @sec-geometry-unions, respectively. Type transformations (from a polygon to a line, for example) are demonstrated in Section @sec-type-transformations.
#
# @sec-geo-ras covers geometric transformations on raster objects. This involves changing the size and number of the underlying pixels, and assigning them new values. It teaches how to change the resolution (also called raster aggregation and disaggregation), the extent and the origin of a raster. These operations are especially useful if one would like to align raster datasets from diverse sources. Aligned raster objects share a one-to-one correspondence between pixels, allowing them to be processed using map algebra operations, described in Section 4.3.2. The final Section 6 connects vector and raster objects. It shows how raster values can be 'masked' and 'extracted' by vector geometries. Importantly it shows how to 'polygonize' rasters and 'rasterize' vector datasets, making the two data models more interchangeable.
#
# ## Geometric operations on vector data {#sec-geo-vec}
#
# ### Simplification {#sec-simplification}
#
# Simplify...

seine_simp = seine.simplify(2000)  # 2000 m

# Plot:

fig, axes = plt.subplots(ncols=2)
seine.plot(ax=axes[0])
seine_simp.plot(ax=axes[1])
axes[0].set_title("Original")
axes[1].set_title("Simplified (d=2000 m)");

# Compare number of nodes:

import sys
sys.getsizeof(seine)       ## Original (bytes)

sys.getsizeof(seine_simp)  ## Simplified (bytes)

# US states example.... Transform...

us_states2163 = us_states.to_crs(2163)

# Simplify...

us_states_simp1 = us_states2163.simplify(100000)

# Plot...

us_states_simp1.plot();

import topojson as tp
topo = tp.Topology(us_states2163, prequantize=False)
us_states_simp2 = topo.toposimplify(100000).to_gdf()

fig, axes = plt.subplots(ncols=3, figsize=(9,5))
us_states2163.plot(ax=axes[0])
us_states_simp1.plot(ax=axes[1])
us_states_simp2.plot(ax=axes[2])
axes[0].set_title("Original")
axes[1].set_title("Simplified (w/ geopandas)")
axes[2].set_title("Simplified (w/ topojson)");

# ### Centroids
#
# Centroid operations identify the center of geographic objects. Like statistical measures of central tendency (including mean and median definitions of 'average'), there are many ways to define the geographic center of an object. All of them create single point representations of more complex vector objects.
#
# The most commonly used centroid operation is the geographic centroid. This type of centroid operation (often referred to as 'the centroid') represents the center of mass in a spatial object (think of balancing a plate on your finger). Geographic centroids have many uses, for example to create a simple point representation of complex geometries, or to estimate distances between polygons. Centroids of the geometries in a `GeoSeries` or a `GeoDataFrame` are accessible through the `.centroid` property, as demonstrated in the code below, which generates the geographic centroids of regions in New Zealand and tributaries to the River Seine, illustrated with black points in Figure ....

nz_centroid = nz.centroid
seine_centroid = seine.centroid

# Sometimes the geographic centroid falls outside the boundaries of their parent objects (think of a doughnut). In such cases point on surface operations can be used to guarantee the point will be in the parent object (e.g., for labeling irregular multipolygon objects such as island states), as illustrated by the red points in Figure .... Notice that these red points always lie on their parent objects. They were created with the `representative_point` method, as follows:

nz_pos = nz.representative_point()
seine_pos = seine.representative_point()

# The centroids and points in surface are illustrated in @fig-centroid-pnt-on-surface:

# +
#| label: fig-centroid-pnt-on-surface
#| fig-cap: "Centroids (black) and points on surface red of New Zealand and Seine datasets."

fig, axes = plt.subplots(ncols=2)
base = nz.plot(ax=axes[0], color="white", edgecolor="lightgrey")
nz_centroid.plot(ax=axes[0], color="None", edgecolor="black")
nz_pos.plot(ax=axes[0], color="None", edgecolor="red");
base = seine.plot(ax=axes[1], color="grey")
seine_centroid.plot(ax=axes[1], color="None", edgecolor="black")
seine_pos.plot(ax=axes[1], color="None", edgecolor="red");
# -

# ### Buffers
#
# Buffers...

seine_buff_5km = seine.buffer(5000)
seine_buff_50km = seine.buffer(50000)

# Plot...

fig, axes = plt.subplots(ncols=2)
seine_buff_5km.plot(ax=axes[0], color="None", edgecolor=["red", "green", "blue"])
seine_buff_50km.plot(ax=axes[1], color="None", edgecolor=["red", "green", "blue"])
axes[0].set_title("5 km buffer")
axes[1].set_title("50 km buffer");

# ### Affine transformations {#sec-affine-transformations}
#
# Affine transformations of `GeoSeries` can be done using the `.affine_transform` method, which is a wrapper around the `shapely.affinity.affine_transform` function. According to the [documentation](https://shapely.readthedocs.io/en/stable/manual.html#shapely.affinity.affine_transform), a 2D affine transformation requires a six-parameter list `[a,b,d,e,xoff,yoff]` which represents the following equations for transforming the coordinates:
#
# $$
# x' = a x + b y + x_\mathrm{off}
# $$
#
# $$
# y' = d x + e y + y_\mathrm{off}
# $$
#
# There are also simplified `GeoSeries` [methods](https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html#affine-transformations) for specific scenarios: 
#
# * `GeoSeries.rotate(angle, origin='center', use_radians=False)`
# *  `GeoSeries.scale(xfact=1.0, yfact=1.0, zfact=1.0, origin='center')`
# *  `GeoSeries.skew(angle, origin='center', use_radians=False)`
# * ` GeoSeries.translate(xoff=0.0, yoff=0.0, zoff=0.0)`
#
# For example, *shifting* only requires the $x_{off}$ and $y_{off}$, using `.translate`. The code below shifts the y-coordinates by 100,000 meters to the north, but leaves the x-coordinates untouched:

nz_shift = nz["geometry"].translate(0, 100000)

# Scale...

nz_scale = nz["geometry"].scale(0.5, 0.5, origin="centroid")

# Rotate...

nz_rotate = nz["geometry"].rotate(-30, origin="centroid")

# Plot... 

fig, axes = plt.subplots(ncols=3, figsize=(9,5))
nz.plot(ax=axes[0], color="lightgrey", edgecolor="darkgrey")
nz_shift.plot(ax=axes[0], color="red", edgecolor="darkgrey")
nz.plot(ax=axes[1], color="lightgrey", edgecolor="darkgrey")
nz_scale.plot(ax=axes[1], color="red", edgecolor="darkgrey")
nz.plot(ax=axes[2], color="lightgrey", edgecolor="darkgrey")
nz_rotate.plot(ax=axes[2], color="red", edgecolor="darkgrey")
axes[0].set_title("Shift")
axes[1].set_title("Scale")
axes[2].set_title("Rotate");

# ### Clipping {#sec-clipping}
#
# ...

# ### Subsetting and clipping
#
# ...

# ### Geometry unions {#sec-geometry-unions}
#
# ...

# ### Type transformations {#sec-type-transformations}
#
# Transformation of geometries, from one type to another, also known as "geometry casting", is often required to facilitate spatial analysis. The `shapely` package can be used for geometry casting. The exact expression(s) depend on the specific transformation we are interested in. In general, you need to figure out the required input of the respective construstor function according to the "destination" geometry (e.g., `shapely.geometry.LineString`, etc.), then reshape the input of the "source" geometry into the right form to be passed to that function.
#
# Let's create a `"MultiPoint"` to illustrate how geometry casting works on `shapely` geometry objects:

multipoint = shapely.geometry.MultiPoint([(1,1), (3,3), (5,1)])
multipoint

# A `"LineString"` can be created using `shapely.geometry.LineString` from a `list` of points. Consequently, a `"MultiPoint"` can be converted to a `"LineString"` by extracting the individual points into a `list`, then passing them to `shapely.geometry.LineString`:

linestring = shapely.geometry.LineString(list(multipoint.geoms))
linestring

# A `"Polygon"` can also be created using funtion `shapely.geometry.Polygon`, which acceps accepts a sequence of points. In principle, the last coordinate must be equal to the first, in order to form a closed shape. However, `shapely.geometry.Polygon` is able to complete the last coordinate automatically. Therefore:

polygon = shapely.geometry.Polygon(list(multipoint.geoms))
polygon

# The source `"MultiPoint"` geometry, and the derived `"LineString"` and `"Polygon"` geometries are shown in @fig-casting1. Note that we convert the `shapely` geometries to `GeoSeries` for easier multi-panel plotting:

# +
#| label: fig-casting1
#| fig-cap: "Examples of linestring and polygon casted from a multipoint geometry."

fig, axes = plt.subplots(ncols=3, figsize=(9,5))
gpd.GeoSeries(multipoint).plot(ax=axes[0])
gpd.GeoSeries(linestring).plot(ax=axes[1])
gpd.GeoSeries(polygon).plot(ax=axes[2])
axes[0].set_title("MultiPoint")
axes[1].set_title("LineString")
axes[2].set_title("Polygon");
# -

# Conversion from multipoint to linestring is a common operation that creates a line object from ordered point observations, such as GPS measurements or geotagged media. This allows spatial operations such as the length of the path traveled. Conversion from multipoint or linestring to polygon is often used to calculate an area, for example from the set of GPS measurements taken around a lake or from the corners of a building lot.
#
# Our `"LineString"` geometry can be converted bact to a `"MultiPoint"` geometry by passing its coordinates directly to `shapely.geometry.MultiPoint`:

# 'LineString' -> 'MultiPoint'
shapely.geometry.MultiPoint(linestring.coords)

# The `"Polygon"` (exterior) coordinates can be passed to `shapely.geometry.MultiPoint` as well:

# 'Polygon' -> 'MultiPoint'
shapely.geometry.MultiPoint(polygon.exterior.coords)

# ...
#
# ## Geometric operations on raster data {#sec-geo-ras}
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
