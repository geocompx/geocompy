#!/usr/bin/env python
# coding: utf-8

# ---
# jupyter: python3
# ---
# 
# # Spatial data operations {#sec-spatial-operations}
# 
# ## Prerequisites {.unnumbered}

# In[ ]:


#| echo: false
import book_options


# In[ ]:


#| echo: false
import book_options_pdf


# This chapter requires importing the following packages:

# In[ ]:


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.ndimage
import scipy.stats
import shapely
import geopandas as gpd
import rasterio
import rasterio.plot
import rasterio.merge
import rasterio.features


# It also relies on the following data files: 

# In[ ]:


#| echo: false
from pathlib import Path
data_path = Path('data')
file_path = Path('data/landsat.tif')
if not file_path.exists():
  if not data_path.is_dir():
     os.mkdir(data_path)
  print('Attempting to get the data')
  import requests
  r = requests.get('https://github.com/geocompx/geocompy/releases/download/0.1/landsat.tif')  
  with open(file_path, 'wb') as f:
    f.write(r.content)


# In[ ]:


nz = gpd.read_file('data/nz.gpkg')
nz_height = gpd.read_file('data/nz_height.gpkg')
world = gpd.read_file('data/world.gpkg')
cycle_hire = gpd.read_file('data/cycle_hire.gpkg')
cycle_hire_osm = gpd.read_file('data/cycle_hire_osm.gpkg')
src_elev = rasterio.open('output/elev.tif')
src_landsat = rasterio.open('data/landsat.tif')
src_grain = rasterio.open('output/grain.tif')


# ## Introduction
# 
# Spatial operations, including spatial joins between vector datasets and local and focal operations on raster datasets, are a vital part of geocomputation. 
# This chapter shows how spatial objects can be modified in a multitude of ways based on their location and shape. Many spatial operations have a non-spatial (attribute) equivalent, so concepts such as subsetting and joining datasets demonstrated in the previous chapter are applicable here.
# This is especially true for vector operations: @sec-vector-attribute-manipulation on vector attribute manipulation provides the basis for understanding its spatial counterpart, namely spatial subsetting (covered in @sec-spatial-subsetting-vector). 
# Spatial joining (@sec-spatial-joining) and aggregation (@sec-vector-spatial-aggregation) also have non-spatial counterparts, covered in the previous chapter.
# 
# Spatial operations differ from non-spatial operations in a number of ways, however. 
# Spatial joins, for example, can be done in a number of ways---including matching entities that intersect with or are within a certain distance of the target dataset---while the attribution joins discussed in @sec-vector-attribute-joining in the previous chapter can only be done in one way.
# Different types of spatial relationships between objects, including intersects and disjoints, are described in @sec-topological-relations.
# Another unique aspect of spatial objects is distance: all spatial objects are related through space, and distance calculations can be used to explore the strength of this relationship, as described in the context of vector data in @sec-distance-relations.
# 
# Spatial operations on raster objects include subsetting---covered in @sec-spatial-subsetting-raster---and merging several raster 'tiles' into a single object, as demonstrated in @sec-merging-rasters.
# Map algebra covers a range of operations that modify raster cell values, with or without reference to surrounding cell values.
# The concept of map algebra, vital for many applications, is introduced in @sec-map-algebra; local, focal, and zonal map algebra operations are covered in sections @sec-raster-local-operations, @sec-focal-operations, and @sec-zonal-operations, respectively. 
# Global map algebra operations, which generate summary statistics representing an entire raster dataset, and distance calculations on rasters, are discussed in Section @sec-global-operations-and-distances.
# 
# ::: callout-note
# It is important to note that spatial operations that use two spatial objects rely on both objects having the same coordinate reference system, a topic that was introduced in @sec-coordinate-reference-systems-intro and which will be covered in more depth in @sec-reproj-geo-data. 
# :::
# 
# ## Spatial operations on vector data {#sec-spatial-vec}
# 
# This section provides an overview of spatial operations on vector geographic data represented as Simple Features using the **shapely** and **geopandas** 
# packages. 
# @sec-spatial-ras then presents spatial operations on raster datasets, using the **rasterio** and **scipy** packages.
# 
# ### Spatial subsetting {#sec-spatial-subsetting-vector}
# 
# <!-- jn: have we considered switching the order of spatial subsetting with topological relations? -->
# <!-- md: I don't think we considered it yet (the order as the moment is the same as in 'geocompr') -->
# 
# Spatial subsetting is the process of taking a spatial object and returning a new object containing only features that relate in space to another object.
# Analogous to attribute subsetting (covered in @sec-vector-attribute-subsetting), subsets of `GeoDataFrame`s can be created with square bracket (`[`) operator using the syntax `x[y]`, where `x` is an `GeoDataFrame` from which a subset of rows/features will be returned, and `y` is a boolean `Series`.
# The difference is, that, in spatial subsetting `y` is created based on another geometry and using one of the binary geometry relation methods, such as `.intersects` (see @sec-topological-relations), rather than based on comparison based on ordinary columns.
# 
# To demonstrate spatial subsetting, we will use the `nz` and `nz_height` layers, which contain geographic data on the 16 main regions and 101 highest points in New Zealand, respectively (@fig-spatial-subset (a)), in a projected coordinate system.
# The following expression creates a new object, `canterbury`, representing only one region --- Canterbury.

# In[ ]:


canterbury = nz[nz['Name'] == 'Canterbury']
canterbury


# Then, we use the `.intersects` method to evaluate, for each of the `nz_height` points, whether they intersect with Canterbury.
# The result `canterbury_height` is a boolean `Series` with the 'answers'.

# In[ ]:


sel = nz_height.intersects(canterbury.geometry.iloc[0])
sel


# Finally, we can subset `nz_height` using the obtained `Series`, resulting in the subset `canterbury_height` with only those points that intersect with Canterbury.

# In[ ]:


canterbury_height = nz_height[sel]
canterbury_height


# @fig-spatial-subset compares the original `nz_height` layer (left) with the subset `canterbury_height` (right).
# <!-- jn: do we need to repeat the `base = nz.plot(color='white', edgecolor='lightgrey')` code here? -->
# <!-- md: The expression to create 'base' has to be repeated. can't say I completely understand the mechanism, but I think that once a 'matplotlib' plot is drawn, the plot objects are emptied, so we have to re-create them when making a new plot. maybe there is a solution to it that I missed, but currently we're creating each plot intependently like in the code below. -->

# In[ ]:


#| label: fig-spatial-subset
#| fig-cap: Spatial subsetting of points by intersection with polygon
#| fig-subcap: 
#| - Original points (red)
#| - Spatial subset based on intersection (red), geometry used for subsetting (Canterbury) (grey)
#| layout-ncol: 2
# Original
base = nz.plot(color='white', edgecolor='lightgrey')
nz_height.plot(ax=base, color='None', edgecolor='red');
# Subset (intersects)
base = nz.plot(color='white', edgecolor='lightgrey')
canterbury.plot(ax=base, color='lightgrey', edgecolor='darkgrey')
canterbury_height.plot(ax=base, color='None', edgecolor='red');


# Like in attribute subsetting (@sec-vector-attribute-subsetting), we are using a boolean series (`sel`), of the same length as the number of rows in the filtered table (`nz_height`), created based on a condition applied on itself.
# The difference is that the condition is not a comparison of attribute values, but an evaluation of a spatial relation.
# Namely, we evaluate whether each geometry of `nz_height` intersects with the `canterbury` geometry, using the `.intersects` method.
# 
# Various topological relations can be used for spatial subsetting which determine the type of spatial relationship that features in the target object must have with the subsetting object to be selected.
# These include touches, crosses, or within, as we will see shortly in @sec-topological-relations.
# Intersects (`.intersects`), which we used in the last example, is the most commonly used method.
# This is a 'catch all' topological relation, that will return features in the target that touch, cross or are within the source 'subsetting' object.
# As an example of another method, we can use `.disjoint` to obtain all points that *do not* intersect with Canterbury.

# In[ ]:


sel = nz_height.disjoint(canterbury.geometry.iloc[0])
canterbury_height2 = nz_height[sel]


# The results are shown in @fig-spatial-subset-disjoint, which compares the original `nz_height` layer (left) with the subset `canterbury_height2` (right).

# In[ ]:


#| label: fig-spatial-subset-disjoint
#| fig-cap: Spatial subsetting of points disjoint from a polygon
#| fig-subcap: 
#| - Original points (red)
#| - Spatial subset based on disjoint (red), geometry used for subsetting (Canterbury) (grey)
#| layout-ncol: 2
# Original
base = nz.plot(color='white', edgecolor='lightgrey')
nz_height.plot(ax=base, color='None', edgecolor='red');
# Subset (disjoint)
base = nz.plot(color='white', edgecolor='lightgrey')
canterbury.plot(ax=base, color='lightgrey', edgecolor='darkgrey')
canterbury_height2.plot(ax=base, color='None', edgecolor='red');


# In case we need to subset according to several geometries at once, e.g., find out which points intersect with both Canterbury and Southland, we can dissolve the filtering subset, using `.union_all`, before applying the `.intersects` (or any other) operator.
# For example, here is how we can subset the `nz_height` points which intersect with Canterbury or Southland.
# (Note that we are also using the `.isin` method, as demonstrated at the end of @sec-vector-attribute-subsetting.)

# In[ ]:


canterbury_southland = nz[nz['Name'].isin(['Canterbury', 'Southland'])]
sel = nz_height.intersects(canterbury_southland.union_all())
canterbury_southland_height = nz_height[sel]
canterbury_southland_height


# @fig-spatial-subset2 shows the results of the spatial subsetting of `nz_height` points by intersection with Canterbury and Southland.

# In[ ]:


#| label: fig-spatial-subset2
#| fig-cap: Spatial subsetting of points by intersection with more than one polygon
#| fig-subcap: 
#| - Original points (red)
#| - Spatial subset based on intersection (red), geometry used for subsetting (Canterbury and Southland) (grey)
#| layout-ncol: 2
# Original
base = nz.plot(color='white', edgecolor='lightgrey')
nz_height.plot(ax=base, color='None', edgecolor='red');
# Subset by intersection with two polygons
base = nz.plot(color='white', edgecolor='lightgrey')
canterbury_southland.plot(ax=base, color='lightgrey', edgecolor='darkgrey')
canterbury_southland_height.plot(ax=base, color='None', edgecolor='red');


# The next section further explores different types of spatial relations, also known as binary predicates (of which `.intersects` and `.disjoint` are two examples), that can be used to identify whether or not two features are spatially related.
# 
# ### Topological relations {#sec-topological-relations}
# 
# Topological relations describe the spatial relationships between objects.
# 'Binary topological relationships', to give them their full name, are logical statements (in that the answer can only be `True` or `False`) about the spatial relationships between two objects defined by ordered sets of points (typically forming points, lines, and polygons) in two or more dimensions [@egenhofer_mathematical_1990].
# That may sound rather abstract and, indeed, the definition and classification of topological relations is based on mathematical foundations first published in book form in 1966 [@spanier_algebraic_1995], with the field of algebraic topology continuing into the 21st century [@dieck_algebraic_2008].
# 
# Despite their mathematical origins, topological relations can be understood intuitively with reference to visualizations of commonly used functions that test for common types of spatial relationships.
# @fig-spatial-relations shows a variety of geometry pairs and their associated relations.
# The third and fourth pairs in @fig-spatial-relations (from left to right and then down) demonstrate that, for some relations, order is important: while the relations equals, intersects, crosses, touches and overlaps are symmetrical, meaning that if `x.relation(y)` is true, `y.relation(x)` will also be true, relations in which the order of the geometries are important such as contains and within are not.
# 
# ::: callout-note
# Notice that each geometry pair has a 'DE-9IM'[^de-9im] string such as `FF2F11212`.
# DE-9IM strings describe the dimensionality (0=points, 1=lines, 2=polygons) of the pairwise intersections of the interior, boundary, and exterior, of two geometries (i.e., nine values of 0/1/2 encoded into a string).
# This is an advanced topic beyond the scope of this book, which can be useful to understand the difference between relation types, or define custom types of relations.
# See the DE-9IM strings section in Geocomputation with R [@lovelace_geocomputation_2019]. 
# Also note that the **shapely** package contains the `.relate` and `.relate_pattern` methods, to derive and to test for DE-9IM patterns, respectively.
# :::
# 
# [^de-9im]: [https://en.wikipedia.org/wiki/DE-9IM](https://en.wikipedia.org/wiki/DE-9IM)
# 
# ![Topological relations between vector geometries, inspired by Figures 1 and 2 in [@egenhofer_mathematical_1990]. The relations for which the `x.relation(y)` is true are printed for each geometry pair, with `x` represented in pink and `y` represented in blue. The nature of the spatial relationship for each pair is described by the Dimensionally Extended 9-Intersection Model string.](images/relations-1.png){#fig-spatial-relations}
# 
# In **shapely**, methods testing for different types of topological relations are known as 'relationships'.
# **geopandas** provides their wrappers (with the same method name) which can be applied on multiple geometries at once (such as `.intersects` and `.disjoint` applied on all points in `nz_height`, see @sec-spatial-subsetting-vector).
# To see how topological relations work in practice, let's create a simple reproducible example, building on the relations illustrated in @fig-spatial-relations and consolidating knowledge of how vector geometries are represented from a previous chapter (@sec-geometry-columns and @sec-geometries).

# In[ ]:


points = gpd.GeoSeries([
  shapely.Point(0.2,0.1), 
  shapely.Point(0.7,0.2), 
  shapely.Point(0.4,0.8)
])
line = gpd.GeoSeries([
  shapely.LineString([(0.4,0.2), (1,0.5)])
])
poly = gpd.GeoSeries([
  shapely.Polygon([(0,0), (0,1), (1,1), (1,0.5), (0,0)])
])


# The sample dataset which we created is composed of three is `GeoSeries`: named `points`, `line`, and `poly`, which are visualized in @fig-spatial-relations-geoms.
# The last expression is a `for` loop used to add text labels (`0`, `1`, and `2`) to identify the points; we are going to explain the concepts of text annotations with **geopandas** `.plot` in @sec-plot-static-labels.

# In[ ]:


#| label: fig-spatial-relations-geoms
#| fig-cap: Points (`points`), line (`line`), and polygon (`poly`) objects used to illustrate topological relations
base = poly.plot(color='lightgrey', edgecolor='red')
line.plot(ax=base, color='black', linewidth=7)
points.plot(ax=base, color='none', edgecolor='black')
for i in enumerate(points):
    base.annotate(
        i[0], xy=(i[1].x, i[1].y), 
        xytext=(3, 3), textcoords='offset points', weight='bold'
    )


# A simple query is: which of the points in `points` intersect in some way with polygon `poly`?
# The question can be answered by visual inspection (points `0` and `2` are touching and are within the polygon, respectively).
# Alternatively, we can get the solution with the `.intersects` method, which reports whether or not each geometry in a `GeoSeries` (`points`) intersects with a single `shapely` geometry (`poly.iloc[0]`).

# In[ ]:


points.intersects(poly.iloc[0])


# The result shown above is a boolean `Series`.
# Its contents should match our intuition: positive (`True`) results are returned for the points `0` and `2`, and a negative result (`False`) for point `1`.
# Each value in this `Series` represents a feature in the first input (`points`).
# 
# All earlier examples in this chapter demonstrate the 'many-to-one' mode of `.intersects` and analogous methods, where the relation is evaluated between each of several geometries in a `GeoSeries`/`GeoDataFrame`, and an individual `shapely` geometry.
# A second mode of those methods (not demonstrated here) is when both inputs are `GeoSeries`/`GeoDataFrame` objects.
# In such case, a 'pairwise' evaluation takes place between geometries aligned by index (`align=True`, the default) or by position (`align=False`).
# For example, the expression `nz.intersects(nz)` returns a `Series` of 16 `True` values, indicating (unsurprisingly) that each geometry in `nz` intersects with itself.
# 
# A third mode is when we are interested in a 'many-to-many' evaluation, i.e., obtaining a matrix of all pairwise combinations of geometries from two `GeoSeries` objects.
# At the time of writing, there is no built-in method to do this in **geopandas**.
# However, the `.apply` method (package **pandas**) can be used to repeat a 'many-to-one' evaluation over all geometries in the second layer, resulting in a matrix of *pairwise* results.
# We will create another `GeoSeries` with two polygons, named `poly2`, to demonstrate this.

# In[ ]:


poly2 = gpd.GeoSeries([
  shapely.Polygon([(0,0), (0,1), (1,1), (1,0.5), (0,0)]),
  shapely.Polygon([(0,0), (1,0.5), (1,0), (0,0)])
])


# Our two input objects, `points` and `poly2`, are illustrated in @fig-spatial-relations-geoms2.

# In[ ]:


#| label: fig-spatial-relations-geoms2
#| fig-cap: Inputs for demonstrating the evaluation of all pairwise intersection relations between three points (`points`) and two polygons (`poly2`)
base = poly2.plot(color='lightgrey', edgecolor='red')
points.plot(ax=base, color='none', edgecolor='black')
for i in enumerate(points):
    base.annotate(
        i[0], xy=(i[1].x, i[1].y), 
        xytext=(3, 3), textcoords='offset points', weight='bold'
    )


# Now we can use `.apply` to get the intersection relations matrix.
# The result is a `DataFrame`, where each row represents a `points` geometry and each column represents a `poly2` geometry.
# We can see that the point `0` intersects with both polygons, while points `1` and `2` intersect with one of the polygons each.

# In[ ]:


points.apply(lambda x: poly2.intersects(x))


# ::: callout-note
# The `.apply` method (package **pandas**) is used to apply a function along one of the axes of a `DataFrame` (or `GeoDataFrame`).
# That is, we can apply a function on all rows (`axis=1`) or all columns (`axis=0`, the default). 
# When the function being applied returns a single value, the output of `.apply` is a `Series` (e.g., `.apply(len)` returns the lengths of all columns, because `len` returns a single value). 
# When the function returns a `Series`, then `.apply` returns a `DataFrame` (such as in the above example.)
# :::
# 
# ::: callout-note
# Since the above result, like any pairwise matrix, (1) is composed of values of the same type, and (2) has no contrasting role for rows and columns, is may be more convenient to use a plain **numpy** array to work with it. 
# In such case, we can use the `.to_numpy` method to go from `DataFrame` to `ndarray`.

# In[ ]:


points.apply(lambda x: poly2.intersects(x)).to_numpy()


# :::
# 
# The `.intersects` method returns `True` even in cases where the features just touch: intersects is a 'catch-all' topological operation which identifies many types of spatial relations, as illustrated in @fig-spatial-relations.
# More restrictive questions include which points lie within the polygon, and which features are on or contain a shared boundary with it?
# The first question can be answered with `.within`, and the second with `.touches`.

# In[ ]:


points.within(poly.iloc[0])


# In[ ]:


points.touches(poly.iloc[0])


# Note that although the point `0` touches the boundary polygon, it is not within it; point `2` is within the polygon but does not touch any part of its border.
# The opposite of `.intersects` is `.disjoint`, which returns only objects that do not spatially relate in any way to the selecting object.

# In[ ]:


points.disjoint(poly.iloc[0])


# Another useful type of relation is 'within distance', where we detect features that intersect with the target buffered by particular distance.
# Buffer distance determines how close target objects need to be before they are selected.
# This can be done by literally buffering (@sec-geometries) the target geometry, and evaluating intersection (`.intersects`).
# Another way is to calculate the distances using the `.distance` method, and then evaluate whether they are within a threshold distance.

# In[ ]:


points.distance(poly.iloc[0]) < 0.2


# Note that although point `1` is more than `0.2` units of distance from the nearest vertex of `poly`, it is still selected when the distance is set to `0.2`.
# This is because distance is measured to the nearest edge, in this case, the part of the polygon that lies directly above point 2 in Figure @fig-spatial-relations.
# We can verify that the actual distance between point `1` and the polygon is `0.13`, as follows.

# In[ ]:


points.iloc[1].distance(poly.iloc[0])


# This is also a good opportunity to repeat that all distance-related calculations in **geopandas** (and **shapely**) assume planar geometry, and only take into account the coordinate values. It is up to the user to make sure that all input layers are in the same projected CRS, so that this type of calculations make sense (see @sec-geometry-operations-on-projected-and-unprojected-data and @sec-when-to-reproject).
# 
# ### Spatial joining {#sec-spatial-joining}
# 
# Joining two non-spatial datasets uses a shared 'key' variable, as described in @sec-vector-attribute-joining.
# Spatial data joining applies the same concept, but instead relies on spatial relations, described in the previous section.
# As with attribute data, joining adds new columns to the target object (the argument `x` in joining functions), from a source object (`y`).
# 
# The following example illustrates the process: imagine you have ten points randomly distributed across the Earth's surface and you ask, for the points that are on land, which countries are they in?
# Implementing this idea in a reproducible example will build your geographic data handling skills and show how spatial joins work.
# The starting point is to create points that are randomly scattered over the planar surface that represents Earth's geographic coordinates, in decimal degrees (@fig-spatial-join (a)).

# In[ ]:


np.random.seed(11)       ## set seed for reproducibility
bb = world.total_bounds  ## the world's bounds
x = np.random.uniform(low=bb[0], high=bb[2], size=10)
y = np.random.uniform(low=bb[1], high=bb[3], size=10)
random_points = gpd.points_from_xy(x, y, crs=4326)
random_points = gpd.GeoDataFrame({'geometry': random_points})
random_points


# The scenario illustrated in @fig-spatial-join shows that the `random_points` object (top left) lacks attribute data, while the world (top right) has attributes, including country names that are shown for a sample of countries in the legend.
# Before creating the joined dataset, we use spatial subsetting to create `world_random`, which contains only countries that contain random points, to verify the number of country names returned in the joined dataset should be four (see the top right panel of @fig-spatial-join (b)).

# In[ ]:


world_random = world[world.intersects(random_points.union_all())]
world_random


# Spatial joins are implemented with `x.sjoin(y)`, as illustrated in the code chunk below.
# The output is the `random_joined` object which is illustrated in @fig-spatial-join (c).

# In[ ]:


random_joined = random_points.sjoin(world, how='left')
random_joined


# @fig-spatial-join shows the input points and countries, the illustration of intersecting countries, and the join result.

# In[ ]:


#| label: fig-spatial-join
#| fig-cap: Illustration of a spatial join
#| fig-subcap: 
#| - A new attribute variable is added to random points,
#| - from source world object,
#| - resulting in points associated with country names
#| layout-ncol: 2
# Random points
base = world.plot(color='white', edgecolor='lightgrey')
random_points.plot(ax=base, color='None', edgecolor='red');
# World countries intersecting with the points
base = world.plot(color='white', edgecolor='lightgrey')
world_random.plot(ax=base, column='name_long');
# Points with joined country names
base = world.plot(color='white', edgecolor='lightgrey')
random_joined.geometry.plot(ax=base, color='grey')
random_joined.plot(ax=base, column='name_long', legend=True);


# ### Non-overlapping joins
# 
# Sometimes two geographic datasets do not touch but still have a strong geographic relationship.
# The datasets `cycle_hire` and `cycle_hire_osm` provide a good example.
# Plotting them reveals that they are often closely related but they do not seem to touch, as shown in @fig-cycle-hire.

# In[ ]:


#| label: fig-cycle-hire
#| fig-cap: The spatial distribution of cycle hire points in London based on official data (blue) and OpenStreetMap data (red). 
base = cycle_hire.plot(edgecolor='blue', color='none')
cycle_hire_osm.plot(ax=base, edgecolor='red', color='none');


# We can check if any of the points are the same by creating a pairwise boolean matrix of `.intersects` relations, then evaluating whether any of the values in it is `True`.
# Note that the `.to_numpy` method is applied to go from a `DataFrame` to an `ndarray`, for which `.any` gives a global rather than a row-wise summary.
# This is what we want in this case, because we are interested in whether any of the points intersect, not whether any of the points in each row intersect.

# In[ ]:


m = cycle_hire.geometry.apply(
  lambda x: cycle_hire_osm.geometry.intersects(x)
)
m.to_numpy().any()


# Imagine that we need to join the capacity variable in `cycle_hire_osm` (`'capacity'`) onto the official 'target' data contained in `cycle_hire`, which looks as follows.

# In[ ]:


cycle_hire


# This is when a non-overlapping join is needed.
# Spatial join (`gpd.sjoin`) along with buffered geometries (see @sec-buffers) can be used to do that, as demonstrated below using a threshold distance of 20 $m$.
# Note that we transform the data to a projected CRS (`27700`) to use real buffer distances, in meters (see @sec-geometry-operations-on-projected-and-unprojected-data).

# In[ ]:


crs = 27700
cycle_hire_buffers = cycle_hire.copy().to_crs(crs)
cycle_hire_buffers.geometry = cycle_hire_buffers.buffer(20)
cycle_hire_buffers = gpd.sjoin(
    cycle_hire_buffers, 
    cycle_hire_osm.to_crs(crs), 
    how='left'
)
cycle_hire_buffers


# Note that the number of rows in the joined result is greater than the target.
# This is because some cycle hire stations in `cycle_hire_buffers` have multiple matches in `cycle_hire_osm`.
# To aggregate the values for the overlapping points and return the mean, we can use the aggregation methods shown in @sec-vector-attribute-aggregation, resulting in an object with the same number of rows as the target.
# We also go back from buffers to points using `.centroid` method.

# In[ ]:


cycle_hire_buffers = cycle_hire_buffers[['id', 'capacity', 'geometry']] \
    .dissolve(by='id', aggfunc='mean') \
    .reset_index()
cycle_hire_buffers.geometry = cycle_hire_buffers.centroid
cycle_hire_buffers


# The capacity of nearby stations can be verified by comparing a plot of the capacity of the source `cycle_hire_osm` data, with the join results in the new object `cycle_hire_buffers` (@fig-cycle-hire-z).

# In[ ]:


#| label: fig-cycle-hire-z
#| fig-cap: Non-overlapping join
#| fig-subcap: 
#| - Input (`cycle_hire_osm`)
#| - Join result (`cycle_hire_buffers`)
#| layout-ncol: 2
# Input
fig, ax = plt.subplots(1, 1, figsize=(6, 3))
cycle_hire_osm.plot(column='capacity', legend=True, ax=ax);
# Join result
fig, ax = plt.subplots(1, 1, figsize=(6, 3))
cycle_hire_buffers.plot(column='capacity', legend=True, ax=ax);


# ### Spatial aggregation {#sec-vector-spatial-aggregation}
# 
# As with attribute data aggregation, spatial data aggregation condenses data: aggregated outputs have fewer rows than non-aggregated inputs.
# Statistical aggregating functions, such as mean, average, or sum, summarize multiple values of a variable, and return a single value per grouping variable.
# @sec-vector-attribute-aggregation demonstrated how the `.groupby` method, combined with summary functions such as `.sum`, condense data based on attribute variables.
# This section shows how grouping by spatial objects can be achieved using spatial joins combined with non-spatial aggregation.
# 
# Returning to the example of New Zealand, imagine you want to find out the average height of `nz_height` points in each region.
# It is the geometry of the source (`nz`) that defines how values in the target object (`nz_height`) are grouped.
# This can be done in three steps:
# 
# 1.  Figuring out which `nz` region each `nz_height` point falls in---using `gpd.sjoin`
# 2.  Summarizing the average elevation per region---using `.groupby` and `.mean`
# 3.  Joining the result back to `nz`---using `pd.merge`
# 
# First, we 'attach' the region classification of each point, using spatial join (@sec-spatial-joining).
# Note that we are using the minimal set of columns required: the geometries (for the spatial join to work), the point elevation (to later calculate an average), and the region name (to use as key when joining the results back to `nz`).
# The result tells us which `nz` region each elevation point falls in.

# In[ ]:


nz_height2 = gpd.sjoin(
  nz_height[['elevation', 'geometry']], 
  nz[['Name', 'geometry']], 
  how='left'
)
nz_height2


# Second, we calculate the average elevation, using ordinary (non-spatial) aggregation (@sec-vector-attribute-aggregation).
# This result tells us the average elevation of all `nz_height` points located within each `nz` region.

# In[ ]:


nz_height2 = nz_height2.groupby('Name')[['elevation']].mean().reset_index()
nz_height2


# The third and final step is joining the averages back to the `nz` layer.

# In[ ]:


nz2 = pd.merge(nz[['Name', 'geometry']], nz_height2, on='Name', how='left')
nz2


# We now have create the `nz2` layer, which gives the average `nz_height` elevation value per polygon.
# The result is shown in @fig-nz-avg-nz-height.
# Note that the `missing_kwds` part determines the style of geometries where the symbology attribute (`elevation`) is missing, because there were no `nz_height` points overlapping with them.
# The default is to omit them, which is usually not what we want, but with `{'color':'grey','edgecolor':'black'}`, those polygons are shown with black outline and grey fill.

# In[ ]:


#| label: fig-nz-avg-nz-height
#| fig-cap: Average height of the top 101 high points across the regions of New Zealand
nz2.plot(
  column='elevation', 
  legend=True,
  cmap='Blues', edgecolor='black',
  missing_kwds={'color': 'grey', 'edgecolor': 'black'}
);


# ### Joining incongruent layers {#sec-joining-incongruent-layers}
# 
# Spatial congruence is an important concept related to spatial aggregation.
# An aggregating object (which we will refer to as `y`) is congruent with the target object (`x`) if the two objects have shared borders.
# Often this is the case for administrative boundary data, whereby larger units---such as Middle Layer Super Output Areas (MSOAs) in the UK, or districts in many other European countries---are composed of many smaller units.
# 
# Incongruent aggregating objects, by contrast, do not share common borders with the target [@qiu_development_2012].
# This is problematic for spatial aggregation (and other spatial operations) illustrated in @fig-nz-and-grid: aggregating the centroid of each sub-zone will not return accurate results.
# Areal interpolation overcomes this issue by transferring values from one set of areal units to another, using a range of algorithms including simple area-weighted approaches and more sophisticated approaches such as 'pycnophylactic' methods [@tobler_smooth_1979].
# 
# To demonstrate joining incongruent layers, we will create a 'synthetic' layer comprising a regular grid of rectangles of size $100\times100$ $km$, covering the extent of the `nz` layer. 
# This recipe can be used to create a regular grid covering any given layer (other than `nz`), at the specified resolution (`res`). 
# Most of the functions have been explained in previous chapters; we leave it as an exercise for the reader to explore how the code works.

# In[ ]:


# Settings: grid extent, resolution, and CRS
bounds = nz.total_bounds
crs = nz.crs
res = 100000
# Calculating grid dimensions
xmin, ymin, xmax, ymax = bounds
cols = list(range(int(np.floor(xmin)), int(np.ceil(xmax+res)), res))
rows = list(range(int(np.floor(ymin)), int(np.ceil(ymax+res)), res))
rows.reverse()
# For each cell, create 'shapely' polygon (rectangle)
polygons = []
for x in cols:
    for y in rows:
        polygons.append(
            shapely.Polygon([(x,y), (x+res, y), (x+res, y-res), (x, y-res)])
        )
# To 'GeoDataFrame'
grid = gpd.GeoDataFrame({'geometry': polygons}, crs=crs)
# Remove rows/columns beyond the extent
sel = grid.intersects(shapely.box(*bounds))
grid = grid[sel]
# Add consecultive IDs
grid['id'] = grid.index
grid


# @fig-nz-and-grid shows the newly created `grid` layer, along with the `nz` layer.

# In[ ]:


#| label: fig-nz-and-grid
#| fig-cap: The `nz` layer, with population size in each region, overlaid with a regular `grid` of rectangles
base = grid.plot(color='none', edgecolor='grey')
nz.plot(
    ax=base, 
    column='Population', 
    edgecolor='black', 
    legend=True, 
    cmap='Reds'
);


# Our goal, now, is to 'transfer' the `'Population'` attribute (@fig-nz-and-grid) to the rectangular grid polygons, which is an example of a join between incongruent layers.
# To do that, we basically need to calculate--for each `grid` cell---the weighted sum of the population in `nz` polygons coinciding with that cell.
# The weights in the weighted sum calculation are the ratios between the area of the coinciding 'part' out of the entire `nz` polygon.
# That is, we (inevitably) assume that the population in each `nz` polygon is equally distributed across space, therefore a partial `nz` polygon contains the respective partial population size.
# 
# We start by calculating the entire area of each `nz` polygon, as follows, using the `.area` method (@sec-area-length).

# In[ ]:


nz['area'] = nz.area
nz


# Next, we use the `.overlay` method to calculate the pairwise intersections between `nz` and `grid`.
# As a result, we now have a layer where each `nz` polygon is split according to the `grid` polygons, hereby named `nz_grid`.

# In[ ]:


nz_grid = nz.overlay(grid)
nz_grid = nz_grid[['id', 'area', 'Population', 'geometry']]
nz_grid


# @fig-nz-and-grid-overlay illustrates the effect of `.overlay`:

# In[ ]:


#| label: fig-nz-and-grid-overlay
#| fig-cap: The pairwise intersections of `nz` and `grid`, calculated with `.overlay`
nz_grid.plot(color='none', edgecolor='black');


# We also need to calculate the areas of the intersections, here into a new attribute `'area_sub'`.
# If an `nz` polygon was completely within a single `grid` polygon, then `area_sub` is going to be equal to `area`; otherwise, it is going to be smaller.

# In[ ]:


nz_grid['area_sub'] = nz_grid.area
nz_grid


# The resulting layer `nz_grid`, with the `area_sub` attribute, is shown in @fig-nz-and-grid2.

# In[ ]:


#| label: fig-nz-and-grid2
#| fig-cap: The areas of pairwise intersections in the `nz_grid` layer
base = grid.plot(color='none', edgecolor='grey')
nz_grid.plot(
    ax=base, 
    column='area_sub', 
    edgecolor='black',
    legend=True, 
    cmap='Reds'
);


# Note that each of the intersections still holds the `Population` attribute of its 'origin' feature of `nz`, i.e., each portion of the `nz` area is associated with the original complete population count for that area.
# The real population size of each `nz_grid` feature, however, is smaller, or equal, depending on the geographic area proportion that it occupies out of the original `nz` feature.
# To make the correction, we first calculate the ratio (`area_prop`) and then multiply it by the population.
# The new (lowercase) attribute `population` now has the correct estimate of population sizes in `nz_grid`:

# In[ ]:


nz_grid['area_prop'] = nz_grid['area_sub'] / nz_grid['area']
nz_grid['population'] = nz_grid['Population'] * nz_grid['area_prop']
nz_grid


# What is left to be done is to sum (see @sec-vector-attribute-aggregation) the population in all parts forming the same grid cell and join (see @sec-vector-attribute-joining) them back to the `grid` layer.
# Note that many of the grid cells have 'No Data' for population, because they have no intersection with `nz` at all (@fig-nz-and-grid).

# In[ ]:


nz_grid = nz_grid.groupby('id')['population'].sum().reset_index()
grid = pd.merge(grid, nz_grid[['id', 'population']], on='id', how='left')
grid


# @fig-nz-and-grid3 shows the final result `grid` with the incongruently-joined `population` attribute from `nz`.

# In[ ]:


#| label: fig-nz-and-grid3
#| fig-cap: 'The `nz` layer and a regular grid of rectangles: final result'
base = grid.plot(
    column='population', 
    edgecolor='black',
    legend=True, 
    cmap='Reds'
);
nz.plot(ax=base, color='none', edgecolor='grey', legend=True);


# We can demonstrate that, expectedly, the summed population in `nz` and `grid` is identical, even though the geometry is different (since we created `grid` to completely cover `nz`), by comparing the `.sum` of the `population` attribute in both layers.

# In[ ]:


nz['Population'].sum()


# In[ ]:


grid['population'].sum()


# The procedure in this section is known as an area-weighted interpolation of a spatially *extensive* (e.g., population) variable.
# In extensive interpolation, we assume that the variable of interest represents counts (such as, here, inhabitants) uniformly distributed across space. 
# In such case, each part of a given polygon captures the respective proportion of counts (such as, half of a region with $N$ inhabitants contains $N/2$ inhabitants).
# Accordingly, summing the parts gives the total count of the total area.
# 
# An area-weighted interpolation of a spatially *intensive* variable (e.g., population density) is almost identical, except that we would have to calculate the weighted `.mean` rather than `.sum`, to preserve the average rather than the sum.
# In intensive interpolation, we assume that the variable of interest represents counts per unit area, i.e., density.
# Since density is (assumed to be) uniform, any part of a given polygon has exactly the same density as that of the whole polygon.
# Density values are therefore computed as weighted averages, rather than sums, of the parts. 
# Also, see the 'Area-weighted interpolation' section in @pebesma_spatial_2023.
# 
# ### Distance relations {#sec-distance-relations}
# 
# While topological relations are binary---a feature either intersects with another or does not---distance relations are continuous.
# The distance between two objects is calculated with the `.distance` method.
# The method is applied on a `GeoSeries` (or a `GeoDataFrame`), with the argument being an individual `shapely` geometry.
# The result is a `Series` of pairwise distances.
# 
# ::: callout-note
# **geopandas** uses similar syntax and mode of operation for many of its methods and functions, including:
# 
# * Numeric calculations, such as `.distance` (this section), returning numeric values
# * Topological evaluation methods, such as `.intersects` or `.disjoint` (@sec-topological-relations), returning boolean values 
# * Geometry generating-methods, such as `.intersection` (@sec-clipping), returning geometries
# 
# In all cases, the input is a `GeoSeries` and (or a `GeoDataFrame`) and a `shapely` geometry, and the output is a `Series` or `GeoSeries` of results, contrasting each geometry from the `GeoSeries` with the `shapely` geometry. 
# The examples in this book demonstrate this, so-called 'many-to-one', mode of the functions. 
# 
# All of the above-mentioned methods also have a pairwise mode, perhaps less useful and not used in the book, where we evaluate relations between pairs of geometries in two `GeoSeries`, aligned either by index or by position. 
# :::
# 
# To illustrate the `.distance` method, let's take the three highest points in New Zealand with `.sort_values` and `.iloc`.

# In[ ]:


nz_highest = nz_height.sort_values(by='elevation', ascending=False).iloc[:3, :]
nz_highest


# Additionally, we need the geographic centroid of the Canterbury region (`canterbury`, created in @sec-spatial-subsetting-vector).

# In[ ]:


canterbury_centroid = canterbury.centroid.iloc[0]


# Now we are able to apply `.distance` to calculate the distances from each of the three elevation points to the centroid of the Canterbury region.

# In[ ]:


nz_highest.distance(canterbury_centroid)


# To obtain a distance matrix, i.e., a pairwise set of distances between all combinations of features in objects `x` and `y`, we need to use the `.apply` method (analogous to the way we created the `.intersects` boolean matrix in @sec-topological-relations).
# To illustrate this, let's now take two regions in `nz`, Otago and Canterbury, represented by the object `co`.

# In[ ]:


sel = nz['Name'].str.contains('Canter|Otag')
co = nz[sel]
co


# The distance matrix (technically speaking, a `DataFrame`) `d` between each of the first three elevation points, and the two regions, is then obtained as follows.
# In plain language, we take the geometry from each each row in `nz_height.iloc[:3,:]`, and apply the `.distance` method on `co` with its rows as the argument.

# In[ ]:


d = nz_height.iloc[:3, :].apply(lambda x: co.distance(x.geometry), axis=1)
d


# Note that the distance between the second and third features in `nz_height` and the second feature in `co` is zero.
# This demonstrates the fact that distances between points and polygons refer to the distance to any part of the polygon: the second and third points in `nz_height` are in Otago, which can be verified by plotting them (two almost completely overlappling points in @fig-nz-height-and-otago).

# In[ ]:


#| label: fig-nz-height-and-otago
#| fig-cap: The first three `nz_height` points, and the Otago and Canterbury regions from `nz`
fig, ax = plt.subplots()
co.plot(color='lightgrey', edgecolor='black', ax=ax)
co.apply(
    lambda x: ax.annotate(
        text=x['Name'], 
        xy=x.geometry.centroid.coords[0], 
        ha='center'
    ), 
    axis=1
)
nz_height.iloc[:3, :].plot(color='none', edgecolor='black', ax=ax);


# ## Spatial operations on raster data {#sec-spatial-ras}
# 
# This section builds on @sec-manipulating-raster-objects, which highlights various basic methods for manipulating raster datasets, to demonstrate more advanced and explicitly spatial raster operations, and uses the `elev.tif` and `grain.tif` rasters manually created in @sec-raster-from-scratch.
# 
# ### Spatial subsetting {#sec-spatial-subsetting-raster}
# 
# The previous chapter (and especially @sec-manipulating-raster-objects) demonstrated how to retrieve values associated with specific row and column combinations from a raster.
# Raster values can also be extracted by location (coordinates) and other spatial objects.
# To use coordinates for subsetting, we can use the `.sample` method of a `rasterio` file connection object, combined with a list of coordinate tuples.
# The method is demonstrated below to find the value of the cell that covers a point located at coordinates of `(0.1,0.1)` in `elev`.
# The returned object is a *generator*. 
# The rationale for returning a generator, rather than a `list`, is memory efficiency. 
# The number of sampled points may be huge, in which case we would want to generate the values one at a time rather than all at once.

# In[ ]:


src_elev.sample([(0.1, 0.1)])


# ::: callout-note
# The technical terms *iterable*, *iterator*, and *generator* in Python may be confusing, so here is a short summary, ordered from most general to most specific:
# 
# * An *iterable* is any object that we can iterate on, such as using a `for` loop. For example, a `list` is iterable. 
# * An *iterator* is an object that represents a stream of data, which we can go over, each time getting the next element using `next`. Iterators are also iterable, meaning that you can over them in a loop, but they are stateful (e.g., they remember which item was obtained using `next`), meaning that you can go over them just once.
# * A *generator* is a function that returns an iterator. For example, the `.sample` method in the above example is a generator. The **rasterio** package makes use of generators in some of its functions, as we will see later on (@sec-raster-to-polygons).
# :::
# 
# In case we nevertheless want all values at once, such as when the number of points is small, we can force the generatrion of all values from a generator at once, using `list`.
# Since there was just one point, the result is one extracted value, in this case `16`.

# In[ ]:


list(src_elev.sample([(0.1, 0.1)]))


# We can use the same technique to extract the values of multiple points at once.
# For example, here we extract the raster values at two points, `(0.1,0.1)` and `(1.1,1.1)`.
# The resulting values are `16` and `6`.

# In[ ]:


list(src_elev.sample([(0.1, 0.1), (1.1, 1.1)]))


# The location of the two sample points on top of the `elev.tif` raster is illustrated in @fig-elev-sample-points.

# In[ ]:


#| label: fig-elev-sample-points
#| fig-cap: The `elev.tif` raster, and two points where we extract its values
fig, ax = plt.subplots()
rasterio.plot.show(src_elev, ax=ax)
gpd.GeoSeries([shapely.Point(0.1, 0.1)]) \
    .plot(color='black', edgecolor='white', markersize=50, ax=ax)
gpd.GeoSeries([shapely.Point(1.1, 1.1)]) \
    .plot(color='black', edgecolor='white', markersize=50, ax=ax);


# ::: callout-note
# We elaborate on the plotting technique used to display the points and the raster in @sec-plot-static-layers.
# We will also introduce a more user-friendly and general method to extract raster values to points, using the **rasterstats** package, in @sec-extraction-to-points.
# :::
# 
# Another common use case of spatial subsetting is using a boolean mask, based on another raster with the same extent and resolution, or the original one, as illustrated in @fig-raster-subset.
# To do that, we erase the values in the array of one raster, according to another corresponding mask raster.
# For example, let's read (@sec-using-rasterio) the `elev.tif` raster values into an array named `elev` (@fig-raster-subset (a)).

# In[ ]:


elev = src_elev.read(1)
elev


# and create a corresponding random boolean mask named `mask` (@fig-raster-subset (b)), of the same shape as `elev.tif` with values randomly assigned to `True` and `False`.

# In[ ]:


np.random.seed(1)
mask = np.random.choice([True, False], src_elev.shape)
mask


# Next, suppose that we want to keep only those values of `elev` which are `False` in `mask` (i.e., they are *not* masked).
# In other words, we want to mask `elev` with `mask`.
# The result will be stored in a copy named `masked_elev` (@fig-raster-subset (c)).
# In the case of `elev.tif`, to be able to store `np.nan` in the array of values, we also need to convert it to `float` (see @sec-summarizing-raster-objects). 
# Afterwards, masking is a matter of assigning `np.nan` into a subset defined by the mask, using the 'boolean array indexing' syntax of **numpy**.

# In[ ]:


masked_elev = elev.copy()
masked_elev = masked_elev.astype('float64')
masked_elev[mask] = np.nan
masked_elev


# @fig-raster-subset shows the original `elev` raster, the `mask` raster, and the resulting `masked_elev` raster.

# In[ ]:


#| label: fig-raster-subset
#| fig-cap: Subsetting raster values using a boolean mask
#| layout-ncol: 3
#| fig-subcap: 
#| - Original raster
#| - Raster mask
#| - Output masked raster
rasterio.plot.show(elev);
rasterio.plot.show(mask);
rasterio.plot.show(masked_elev);


# The mask can be created from the array itself, using condition(s). 
# That way, we can replace some values (e.g., values assumed to be wrong) with `np.nan`, such as in the following example.

# In[ ]:


elev2 = elev.copy()
elev2 = elev2.astype('float64')
elev2[elev2 < 20] = np.nan
elev2


# This technique is also used to reclassify raster values (see @sec-raster-local-operations).
# 
# ### Map algebra {#sec-map-algebra}
# 
# The term 'map algebra' was coined in the late 1970s to describe a 'set of conventions, capabilities, and techniques' for the analysis of geographic raster and (although less prominently) vector data [@tomlin_map_1994].
# In this context, we define map algebra more narrowly, as operations that modify or summarize raster cell values, with reference to surrounding cells, zones, or statistical functions that apply to every cell.
# 
# Map algebra operations tend to be fast, because raster datasets only implicitly store coordinates, hence the old adage 'raster is faster but vector is corrector'.
# The location of cells in raster datasets can be calculated by using its matrix position and the resolution and origin of the dataset (stored in the raster metadata, @sec-using-rasterio).
# For the processing, however, the geographic position of a cell is barely relevant as long as we make sure that the cell position is still the same after the processing.
# Additionally, if two or more raster datasets share the same extent, projection, and resolution, one could treat them as matrices for the processing.
# 
# Map algebra (or cartographic modeling with raster data) divides raster operations into four subclasses [@tomlin_geographic_1990], with each working on one or several grids simultaneously:
# 
# -   Local or per-cell operations (@sec-raster-local-operations)
# -   Focal or neighborhood operations. Most often the output cell value is the result of a $3 \times 3$ input cell block (@sec-focal-operations)
# -   Zonal operations are similar to focal operations, but the surrounding pixel grid on which new values are computed can have irregular sizes and shapes (@sec-zonal-operations)
# -   Global or per-raster operations; that means the output cell derives its value potentially from one or several entire rasters (@sec-global-operations-and-distances)
# 
# This typology classifies map algebra operations by the number of cells used for each pixel processing step and the type of output.
# For the sake of completeness, we should mention that raster operations can also be classified by disciplines such as terrain, hydrological analysis, or image classification.
# The following sections explain how each type of map algebra operations can be used, with reference to worked examples.
# 
# ### Local operations {#sec-raster-local-operations}
# 
# Local operations comprise all cell-by-cell operations in one or several layers.
# Raster algebra is a classical use case of local operations---this includes adding or subtracting values from a raster, squaring,, and multiplying rasters.
# Raster algebra also allows logical operations such as finding all raster cells that are greater than a specific value (e.g., `5` in our example below).
# Local operations are applied using the **numpy** array operations syntax, as demonstrated below.
# 
# First, let's take the array of `elev.tif` raster values, which we already read earlier (@sec-spatial-subsetting-raster).

# In[ ]:


elev


# Now, any element-wise array operation can be applied using **numpy** arithmetic or conditional operators and functions, comprising local raster operations in spatial analysis terminology.
# For example, `elev + elev` adds the values of `elev` to itself, resulting in a raster with double values.

# In[ ]:


elev + elev


# Note that some functions and operators automatically change the data type to accommodate the resulting values, while other operators do not, potentially resulting in overflow (i.e., incorrect values for results beyond the data type range, such as trying to accommodate values above `255` in an `int8` array).
# For example, `elev**2` (`elev` squared) results in overflow.
# Since the `**` operator does not automatically change the data type, leaving it as `int8`, the resulting array has incorrect values for `16**2`, `17**2`, etc., which are above `255` and therefore cannot be accommodated.

# In[ ]:


elev**2


# To avoid this situation, we can, for instance, transform `elev` to the standard `int64` data type, using `.astype` before applying the `**` operator.
# That way, all results, up to `36**2` (`1296`), can be easily accommodated, since the `int64` data type supports values up to `9223372036854775807` (@tbl-numpy-data-types).

# In[ ]:


elev.astype(int)**2


# Now we get correct results.
# 
# @fig-raster-local-operations demonstrates the result of the last two examples (`elev+elev` and `elev.astype(int)**2`), and two other ones (`np.log(elev)` and `elev>5`).

# In[ ]:


#| label: fig-raster-local-operations
#| fig-cap: 'Examples of different local operations of the elev raster object: adding two rasters, squaring, applying logarithmic transformation, and performing a logical operation.'
#| layout-ncol: 4
#| fig-subcap: 
#| - '`elev+elev`'
#| - '`elev.astype(int)**2`'
#| - '`np.log(elev)`'
#| - '`elev>5`'
rasterio.plot.show(elev + elev, cmap='Oranges');
rasterio.plot.show(elev.astype(int)**2, cmap='Oranges');
rasterio.plot.show(np.log(elev), cmap='Oranges');
rasterio.plot.show(elev > 5, cmap='Oranges');


# Another good example of local operations is the classification of intervals of numeric values into groups such as grouping a digital elevation model into low (class `1`), middle (class `2`) and high (class `3`) elevations.
# Here, the raster values in the ranges `0`--`12`, `12`--`24`, and `24`--`36` are reclassified to take values `1`, `2`, and `3`, respectively.

# In[ ]:


recl = elev.copy()
recl[(elev > 0)  & (elev <= 12)] = 1
recl[(elev > 12) & (elev <= 24)] = 2
recl[(elev > 24) & (elev <= 36)] = 3


# @fig-raster-reclassify compares the original `elev` raster with the reclassified `recl` one.

# In[ ]:


#| label: fig-raster-reclassify
#| fig-cap: Reclassifying a continuous raster into three categories.
#| layout-ncol: 2
#| fig-subcap: 
#| - Original
#| - Reclassified
rasterio.plot.show(elev, cmap='Oranges');
rasterio.plot.show(recl, cmap='Oranges');


# The calculation of the Normalized Difference Vegetation Index (NDVI)[^ndvi] is a well-known local (pixel-by-pixel) raster operation.
# It returns a raster with values between `-1` and `1`; positive values indicate the presence of living plants (mostly \> `0.2`).
# NDVI is calculated from red and near-infrared (NIR) bands of remotely sensed imagery, typically from satellite systems such as Landsat or Sentinel-2.
# Vegetation absorbs light heavily in the visible light spectrum, and especially in the red channel, while reflecting NIR light, which is emulated in the NVDI formula (@eq-ndvi),
# 
# [^ndvi]: [https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index](https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index)
# 
# $$
# NDVI=\frac{NIR-Red} {NIR+Red}
# $$ {#eq-ndvi}
# 
# , where $NIR$ is the near-infrared band and $Red$ is the red band.
# 
# Let's calculate NDVI for the multispectral Landsat satellite file (`landsat.tif`) of the Zion National Park.
# The file `landsat.tif` contains surface reflectance values (range `0`-`1`) in the blue, green, red, and near-infrared (NIR) bands.
# We start by reading the file and extracting the NIR and red bands, which are the fourth and third bands, respectively.
# Next, we apply the formula to calculate the NDVI values.

# In[ ]:


#| warning: false
landsat = src_landsat.read()
nir = landsat[3]
red = landsat[2]
ndvi = (nir-red)/(nir+red)


# When plotting an RGB image using the `rasterio.plot.show` function, the function assumes that values are in the range `[0,1]` for floats, or `[0,255]` for integers (otherwise clipped) and the order of bands is RGB.
# To prepare the multi-band raster for `rasterio.plot.show`, we, therefore, reverse the order of the first three bands (to go from B-G-R-NIR to R-G-B), using the `[:3]` slice to select the first three bands and then the `[::-1]` slice to reverse the bands order, and divide by the raster maximum to set the maximum value to `1`.

# In[ ]:


landsat_rgb = landsat[:3][::-1] / landsat.max()


# ::: callout-note
# Python slicing notation, which **numpy**, **pandas** and **geopandas** also follow, is `object[start:stop:step]`. 
# The default is to start from the beginning, go to the end, and use steps of `1`. 
# Otherwise, `start` is inclusive and `end` is exclusive, whereas negative `step` values imply going backwards starting from the end. 
# Also, always keep in mind that Python indices start from `0`.
# When subsetting two- or three-dimensional objects, indices for each dimension are separated by commas, where either index can be set to `:` meaning 'all values'.
# The last dimensions can also be omitted implying `:`, e.g., to subset the first three bands from a three-dimensional array `a` we can use either `a[:3,:,:]` or `a[:3]`.
# 
# In the above example: 
# 
# * The slicing expression `[:3]` therefore means layers `0`, `1`, `2` (up to `3`, exclusive)
# * The slicing expression `[::-1]` therefore means all (three) bands in reverse order
# :::
# 
# @fig-raster-ndvi shows the RGB image and the NDVI values calculated for the Landsat satellite image of the Zion National Park.

# In[ ]:


#| label: fig-raster-ndvi
#| fig-cap: RGB image and NDVI values calculated for the Landsat satellite image of the Zion National Park
#| layout-ncol: 2
#| fig-subcap: 
#| - RGB image
#| - NDVI
rasterio.plot.show(landsat_rgb, cmap='RdYlGn');
rasterio.plot.show(ndvi, cmap='Greens');


# ### Focal operations {#sec-focal-operations}
# 
# While local functions operate on one cell at a time (though possibly from multiple layers), focal operations take into account a central (focal) cell and its neighbors.
# The neighborhood (also named kernel, filter, or moving window) under consideration is typically of $3 \times 3$ cells (that is, the central cell and its eight surrounding neighbors), but can take on any other (not necessarily rectangular) shape as defined by the user.
# A focal operation applies an aggregation function to all cells within the specified neighborhood, uses the corresponding output as the new value for the central cell, and moves on to the next central cell (@fig-focal-filter).
# Other names for this operation are spatial filtering and convolution [@burrough_principles_2015].
# 
# ![Input raster (left) and resulting output raster (right) due to a focal operation---finding the minimum value in $3 \times 3$ moving windows.](images/04_focal_example.png){#fig-focal-filter}
# 
# In Python, the **scipy.ndimage** [@scipy] package has a comprehensive collection of functions to perform filtering of **numpy** arrays, such as:
# 
# -   `scipy.ndimage.minimum_filter`,
# -   `scipy.ndimage.maximum_filter`,
# -   `scipy.ndimage.uniform_filter` (i.e., mean filter),
# -   `scipy.ndimage.median_filter`, etc.
# 
# In this group of functions, we define the shape of the moving window with either one of `size`---a single number (e.g., `3`), or tuple (e.g., `(3,3)`), implying a filter of those dimensions, or `footprint`---a boolean array, representing both the window shape and the identity of elements being included.
# 
# In addition to specific built-in filters, `convolve`---applies the sum function after multiplying by a custom `weights` array, and `generic_filter`---makes it possible to pass any custom function, where the user can specify any type of custom window-based calculation.
# 
# For example, here we apply the minimum filter with window size of `3` on `elev`.
# As a result, we now have a new array `elev_min`, where each value is the minimum in the corresponding $3 \times 3$ neighborhood in `elev`.

# In[ ]:


elev_min = scipy.ndimage.minimum_filter(elev, size=3)
elev_min


# Special care should be given to the edge pixels -- how should they be calculated?
# The **scipy.ndimage** filtering functions give several options through the `mode` parameter (see the documentation of any filtering function, such as `scipy.ndimage.median_filter`, for the definition of each mode): `reflect` (the default), `constant`, `nearest`, `mirror`, `wrap`.
# Sometimes artificially extending raster edges is considered unsuitable.
# In other words, we may wish the resulting raster to contain pixel values with 'complete' windows only, for example, to have a uniform sample size or because values in all directions matter (such as in topographic calculations).
# There is no specific option *not* to extend edges in **scipy.ndimage**.
# However, to get the same effect, the edges of the filtered array can be assigned with `np.nan`, in a number of rows and columns according to filter size.
# For example, when using a filter of `size=3`, the outermost 'layer' of pixels may be assigned with `np.nan`, reflecting the fact that these pixels have incomplete $3 \times 3$ neighborhoods (@fig-focal-filter):

# In[ ]:


elev_min = elev_min.astype(float)
elev_min[:, [0, -1]] = np.nan
elev_min[[0, -1], :] = np.nan
elev_min


# We can quickly check if the output meets our expectations.
# In our example, the minimum value has to be always the upper left corner of the moving window (remember we have created the input raster by row-wise incrementing the cell values by one starting at the upper left corner).
# 
# Focal functions or filters play a dominant role in image processing.
# For example, low-pass or smoothing filters use the mean function to remove extremes.
# By contrast, high-pass filters, often created with custom neighborhood weights, accentuate features.
# 
# In the case of categorical data, we can replace the mean with the mode, i.e., the most common value.
# To demonstrate applying a mode filter, let's read the small sample categorical raster `grain.tif`.

# In[ ]:


grain = src_grain.read(1)
grain


# There is no built-in filter function for a mode filter in **scipy.ndimage**, but we can use the `scipy.ndimage.generic_filter` function along with a custom filtering function, internally utilizing `scipy.stats.mode`. 

# In[ ]:


grain_mode = scipy.ndimage.generic_filter(
    grain, 
    lambda x: scipy.stats.mode(x.flatten())[0], 
    size=3
)
grain_mode = grain_mode.astype(float)
grain_mode[:, [0, -1]] = np.nan
grain_mode[[0, -1], :] = np.nan
grain_mode


# ::: callout-note
# `scipy.stats.mode` is a function to summarize array values, returning the mode (most common value). It is analogous to **numpy** summary functions and methods, such as `.mean` or `.max`. **numpy** itself does not provide the *mode* function, however, which is why we use **scipy** for that.
# :::
# 
# Terrain processing is another important application of focal operations.
# Such functions are provided by multiple Python packages, including the general purpose **xarray** package, and more specialized packages such as **richdem** and **pysheds**.
# Useful terrain metrics include:
# 
# -   Slope, measured in units of percent, degreees, or radians [@horn_1981]
# -   Aspect, meaning each cell's downward slope direction [@horn_1981]
# -   Slope curvature, including 'planform' and 'profile' curvature [@zevenbergen_1987]
# 
# For example, each of these, and other, terrain metrics can be computed with the **richdem** package.
# 
# ::: callout-note
# Terrain metrics are essentially focal filters with customized functions. 
# Using `scipy.ndimage.generic_filter`, along with such custom functions, is an option for those who would like to calculate terrain metric through coding by hand and/or limiting their code dependencies.
# For example, the *How Aspect works*[^how_aspect_works] and *How Slope works*[^how_slope_works] pages from the ArcGIS Pro documentation provide explanations and formulas of the required functions for aspect and slope metrics (@fig-raster-slope), respectively, which can be translated to **numpy**-based functions to be used in `scipy.ndimage.generic_filter` to calculate those metrics.
# :::
# 
# [^how_aspect_works]: [https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-aspect-works.htm](https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-aspect-works.htm)
# 
# [^how_slope_works]: [https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-slope-works.htm](https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-slope-works.htm)
# 
# Another extremely fast, memory-efficient, and concise, alternative, is to the use the GDAL program called `gdaldem`.
# `gdaldem` can be used to calculate slope, aspect, and other terrain metrics through a single command, accepting an input file path and exporting the result to a new file.
# This is our first example in the book where we demonstrate a situation where it may be worthwhile to leave the Python environment, and utilize a GDAL program directly, rather than through their wrappers (such as **rasterio** and other Python packages), whether to access a computational algorithm not easily accessible in a Python package, or for GDAL's memory-efficiency and speed benefits.
# 
# ::: callout-note
# GDAL contains a collection of over 40 programs, mostly aimed at raster processing. These include programs for fundamental operations, such as:
# 
# * `gdal_translate`---convert between raster file formats
# * `gdalwarp`---raster reprojection
# * `gdal_rasterize`---rasterize vector features
# * `gdal_merge.py`---raster mosaic 
# 
# In this book, we use **rasterio** for the above-mentioned operations, although the GDAL programs are a good alternative for those who are more comfortable with the command line. However, we do use two GDAL programs for tasks that are lacking in **rasterio** and not well-implemented in other Python packages: `gdaldem` (this section), and `gdal_contour` (@sec-raster-to-contours).
# :::
# 
# GDAL, along with all of its programs should be available in your Python environment, since GDAL is a dependency of **rasterio**.
# The following example, which should be run from the command line, takes the `srtm_32612.tif` raster (which we are going to create in @sec-reprojecting-raster-geometries, therefore it is in the `'output'` directory), calculates slope (in decimal degrees, between `0` and `90`), and exports the result to a new file `srtm_32612_slope.tif`.
# Note that the arguments of `gdaldem` are the metric name (`slope`), then the input file path, and finally the output file path.

# In[ ]:


#| eval: false
os.system('gdaldem slope output/srtm_32612.tif output/srtm_32612_slope.tif')


# Here we ran the `gdaldem` command through `os.system`, in order to remain in the Python environment, even though we are calling an external program.
# Alternatively, you can run the standalone command in the command line interface you are using, such as the Anaconda Prompt:
# 
# ```{sh}
# gdaldem slope output/srtm_32612.tif output/srtm_32612_slope.tif
# ```
# 
# Replacing the metric name, we can calculate other terrain properties.
# For example, here is how we can calculate an aspect raster `srtm_32612_aspect.tif`, also in degrees (between `0` and `360`).

# In[ ]:


#| eval: false
os.system('gdaldem aspect output/srtm_32612.tif output/srtm_32612_aspect.tif')


# @fig-raster-slope shows the results, using our more familiar plotting methods from **rasterio**.
# The code section is relatively long due to the workaround to create a color key (see @sec-plot-symbology) and removing 'No Data' flag values from the arrays so that the color key does not include them. Also note that we are using one of **matplotlib**'s the cyclic color scales (`'twilight'`) when plotting aspect (@fig-raster-slope (c)).

# In[ ]:


#| label: fig-raster-slope
#| fig-cap: Slope and aspect calculation from a DEM
#| layout-ncol: 3
#| fig-subcap: 
#| - Input DEM
#| - Slope (degrees)
#| - Aspect (degrees)
# Input DEM
src_srtm = rasterio.open('output/srtm_32612.tif')
srtm = src_srtm.read(1).astype(float)
srtm[srtm == src_srtm.nodata] = np.nan
fig, ax = plt.subplots()
rasterio.plot.show(src_srtm, cmap='Spectral_r', ax=ax)
fig.colorbar(ax.imshow(srtm, cmap='Spectral_r'), ax=ax);
# Slope
src_srtm_slope = rasterio.open('output/srtm_32612_slope.tif')
srtm_slope = src_srtm_slope.read(1)
srtm_slope[srtm_slope == src_srtm_slope.nodata] = np.nan
fig, ax = plt.subplots()
rasterio.plot.show(src_srtm_slope, cmap='Spectral_r', ax=ax)
fig.colorbar(ax.imshow(srtm_slope, cmap='Spectral_r'), ax=ax);
# Aspect
src_srtm_aspect = rasterio.open('output/srtm_32612_aspect.tif')
srtm_aspect = src_srtm_aspect.read(1)
srtm_aspect[srtm_aspect == src_srtm_aspect.nodata] = np.nan
fig, ax = plt.subplots()
rasterio.plot.show(src_srtm_aspect, cmap='twilight', ax=ax)
fig.colorbar(ax.imshow(srtm_aspect, cmap='twilight'), ax=ax);


# ### Zonal operations {#sec-zonal-operations}
# 
# Just like focal operations, zonal operations apply an aggregation function to multiple raster cells.
# However, a second raster, usually with categorical values, defines the zonal filters (or 'zones') in the case of zonal operations, as opposed to a predefined neighborhood window in the case of focal operation presented in the previous section.
# Consequently, raster cells defining the zonal filter do not necessarily have to be neighbors.
# Our `grain.tif` raster is a good example, as illustrated in @fig-rasterio-plot-grain: different grain sizes are spread irregularly throughout the raster.
# Finally, the result of a zonal operation is a summary table grouped by zone, which is why this operation is also known as zonal statistics in the GIS world.
# This is in contrast to focal operations (@sec-focal-operations) which return a raster object.
# 
# To demonstrate, let's get back to the `grain.tif` and `elev.tif` rasters.
# To calculate zonal statistics, we use the arrays with raster values, which we already imported earlier.
# Our intention is to calculate the average (or any other summary function, for that matter) of *elevation* in each zone defined by *grain* values.
# To do that, first we first obtain the unique values defining the zones using `np.unique`.

# In[ ]:


np.unique(grain)


# Now, we can use dictionary comprehension (see note below) to split the `elev` array into separate one-dimensional arrays with values per `grain` group, with keys being the unique `grain` values.

# In[ ]:


z = {i: elev[grain == i] for i in np.unique(grain)}
z


# ::: callout-note
# *List comprehension* and *dictionary comprehension* are concise ways to create a `list` or a `dict`, respectively, from an iterable object.
# Both are, conceptually, a concise syntax to replace `for` loops where we iterate over an object and return a same-length object with the results.
# Here are minimal examples of list and dictionary comprehension, respectively, to demonstrate the idea:
# 
# * `[i**2 for i in [2,4,6]]`---Returns `[4,16,36]`
# * `{i: i**2 for i in [2,4,6]}`---Returns `{2:4, 4:16, 6:36}`
# 
# List comprehension is more commonly encountered in practice. We use it in @sec-subsetting-vs-clipping, @sec-rasterizing-lines-and-polygons, @sec-raster-to-polygons, and @sec-distance-to-nearest-geometry. Dictionary comprehension is only used in one place in the book (this section).
# :::
# 
# At this stage, we can expand the dictionary comprehension expression to calculate the mean elevation associated with each grain size class.
# Namely, instead of placing the elevation values (`elev[grain==i]`) into the dictionary values, we place their (rounded) mean (`elev[grain==i].mean().round(1)`).

# In[ ]:


z = {i: elev[grain == i].mean().round(1) for i in np.unique(grain)}
z


# This returns the statistics for each category, here the mean elevation for each grain size class.
# For example, the mean elevation in pixels characterized by grain size `0` is `14.8`, and so on.
# 
# ### Global operations and distances {#sec-global-operations-and-distances}
# 
# Global operations are a special case of zonal operations with the entire raster dataset representing a single zone.
# The most common global operations are descriptive statistics for the entire raster dataset such as the minimum or maximum---we already discussed those in @sec-summarizing-raster-objects.
# 
# Aside from that, global operations are also useful for the computation of distance and weight rasters.
# In the first case, one can calculate the distance from each cell to specific target cells or vector geometries.
# For example, one might want to compute the distance to the nearest coast (see @sec-distance-to-nearest-geometry).
# We might also want to consider topography, that means, we are not only interested in the pure distance but would like also to avoid the crossing of mountain ranges when going to the coast.
# To do so, we can weight the distance with elevation so that each additional altitudinal meter 'prolongs' the Euclidean distance (this is beyond the scope of the book).
# Visibility and viewshed computations also belong to the family of global operations (also beyond the scope of the book).
# 
# ### Map algebra counterparts in vector processing
# 
# Many map algebra operations have a counterpart in vector processing [@liu_essential_2009].
# Computing a distance raster (global operation) while only considering a maximum distance (logical focal operation) is the equivalent of a vector buffer operation (@sec-buffers).
# Reclassifying raster data (either local or zonal function depending on the input) is equivalent to dissolving vector data (@sec-geometry-unions).
# Overlaying two rasters (local operation), where one contains 'No Data' values representing a mask, is similar to vector clipping (Section @sec-clipping).
# Quite similar to spatial clipping is intersecting two layers (@sec-spatial-subsetting-vector, @sec-joining-incongruent-layers).
# The difference is that these two layers (vector or raster) simply share an overlapping area.
# However, be careful with the wording.
# Sometimes the same words have slightly different meanings for raster and vector data models.
# While aggregating polygon geometries means dissolving boundaries, for raster data geometries it means increasing cell sizes and thereby reducing spatial resolution.
# Zonal operations dissolve the cells of one raster in accordance with the zones (categories) of another raster dataset using an aggregating function.
# 
# ### Merging rasters {#sec-merging-rasters}
# 
# Suppose we would like to compute the NDVI (see @sec-raster-local-operations), and additionally want to compute terrain attributes from elevation data for observations within a study area.
# Such computations rely on remotely sensed information.
# The corresponding source imagery is often divided into scenes covering a specific spatial extent (i.e., tiles), and frequently, a study area covers more than one scene.
# Then, we would need to merge (also known as mosaic) the scenes covering our study area.
# In case when all scenes are aligned (i.e., share the same origin and resolution), this can be thought of as simply gluing them into one big raster; otherwise, all scenes need to be resampled (see @sec-raster-resampling) to the same grid (e.g., the one defined by the first scene).
# 
# For example, let's merge digital elevation data from two SRTM elevation tiles, for Austria (`'aut.tif'`) and Switzerland (`'ch.tif'`).
# Merging can be done using function `rasterio.merge.merge`, which accepts a `list` of raster file connections, and returns the new `ndarray` and the corresponding transform object, representing the resulting mosaic.

# In[ ]:


src_1 = rasterio.open('data/aut.tif')
src_2 = rasterio.open('data/ch.tif')
out_image, out_transform = rasterio.merge.merge([src_1, src_2])


# ::: callout-note
# Some Python packages (such as `rasterio`) are split into several so-called sub-modules. 
# The sub-modules are installed collectively when installing the main package.
# However, each sub-module needs to be loaded separately to be able to use its functions. 
# For example, the `rasterio.merge.merge` function (see last code block) comes from the `rasterio.merge` sub-module of `rasterio`.
# Loading `rasterio` with `import rasterio` does not expose the `rasterio.merge.merge` function; instead, we have to load `rasterio.merge` with `import rasterio.merge`, and only then use `rasterio.merge.merge`. 
# 
# Also check out the first code block in this chapter, where we load `rasterio` as well as three sub-modules: `rasterio.plot`, `rasterio.merge`, and `rasterio.features`.
# :::
# 
# @fig-raster-merge shows both inputs and the resulting mosaic.

# In[ ]:


#| label: fig-raster-merge
#| fig-cap: Raster merging
#| layout-ncol: 3
#| fig-subcap: 
#| - '`aut.tif`'
#| - '`ch.tif`'
#| - Mosaic (`aut.tif`+`ch.tif`)
rasterio.plot.show(src_1);
rasterio.plot.show(src_2);
rasterio.plot.show(out_image, transform=out_transform);


# By default in `rasterio.merge.merge`, areas of overlap retain the value of the *first* raster (`method='first'`).
# Other possible methods are:
# 
# -   `'last'`---Value of the last raster
# -   `'min'`---Minimum value
# -   `'max'`---Maximum value
# 
# When dealing with non-overlapping tiles, such as `aut.tif` and `ch.tif` (above), the `method` argument has no practical effect.
# However, it becomes relevant when we want to combine spectral imagery from scenes that were taken on different dates.
# The above four options for `method` do not cover the commonly required scenario when we would like to compute the *mean* value---for example to calculate a seasonal average NDVI image from a set of partially overlapping satellite images (such as Landsat).
# An alternative workflow to `rasterio.merge.merge`, for calculating a mosaic as well as averaging any overlaps, is to go through two steps:
# 
# -   Resampling all scenes into a common 'global' grid (@sec-raster-resampling), thereby producing a series of matching rasters (with the area surrounding each scene set as 'No Data')
# -   Averaging the rasters through raster algebra (@sec-raster-local-operations), using `np.mean(m,axis=0)` or `np.nanmean(m,axis=0)` (depending whether we prefer to ignore 'No Data' or not), where `m` is the multi-band array, which would return a single-band array of averages
# 
# <!-- ## Exercises
# 
# -   Write a function which accepts and array and an `int` specifying the number of rows/columns to erase along an array edges. The function needs to return the modified array with `np.nan` values along its edges. -->
# 
