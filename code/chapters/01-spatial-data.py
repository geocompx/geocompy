#!/usr/bin/env python
# coding: utf-8

# # Geographic data in Python {#sec-spatial-class}
# 
# ## Introduction
# 
# This chapter outlines two fundamental geographic data models --- vector and raster --- and introduces the main Python packages for working with them.
# Before demonstrating their implementation in Python, we will introduce the theory behind each data model and the disciplines in which they predominate.
# 
# The vector data model (@sec-vector-data) represents the world using points, lines, and polygons.
# These have discrete, well-defined borders, meaning that vector datasets usually have a high level of precision (but not necessarily accuracy).
# The raster data model (@sec-raster-data), on the other hand, divides the surface up into cells of constant size.
# Raster datasets are the basis of background images used in web-mapping and have been a vital source of geographic data since the origins of aerial photography and satellite-based remote sensing devices.
# Rasters aggregate spatially specific features to a given resolution, meaning that they are consistent over space and scalable, with many worldwide raster datasets available.
# 
# Which to use?
# The answer likely depends on your domain of application, and the datasets you have access to:
# 
# -   Vector datasets and methods dominate the social sciences because human settlements and processes (e.g., transport infrastructure) tend to have discrete borders<!--jn: is that true?--> <!-- md: I think that's true but now sure how we can back up this idea, will be happy to hear what everyone thinks -->
# -   Raster datasets and methods dominate many environmental sciences because of the reliance on remote sensing data
# 
# Python has strong support for both data models.
# We will focus on **shapely** and **geopandas** for working with geograpic vector data, and **rasterio** for working with rasters.
# 
# **shapely** is a "low-level" package for working with individual vector geometry objects.
# **geopandas** is a "high-level" package for working with geometry columns (`GeoSeries` objects), which internally contain **shapely** geometries, and vector layers (`GeoDataFrame` objects).
# The **geopandas** ecosystem provides a comprehensive approach for working with vector layers in Python, with many packages building on it.
# 
# There are several partially overlapping packages for working with raster data, each with its own advantages and disadvantages.
# In this book, we focus on the most prominent one: **rasterio**, which represents "simple" raster datasets with a combination of a **numpy** array, and a metadata object (`dict`) providing geographic metadata such as the coordinate system.
# **xarray** is a notable alternative to **rasterio** not covered in this book which uses native `xarray.Dataset` and `xarray.DataArray` classes to effectively represent complex raster datasets such as NetCDF files with multiple bands and metadata.
# 
# There is much overlap in some fields and raster and vector datasets can be used together: ecologists and demographers, for example, commonly use both vector and raster data.
# Furthermore, it is possible to convert between the two forms (see @sec-raster-vector).
# Whether your work involves more use of vector or raster datasets, it is worth understanding the underlying data models before using them, as discussed in subsequent chapters.
# 
# ## Vector data {#sec-vector-data}
# 
# The geographic vector data model is based on points located within a coordinate reference system (CRS).
# Points can represent self-standing features (e.g., the location of a bus stop), or they can be linked together to form more complex geometries such as lines and polygons.
# Most point geometries contain only two dimensions (three-dimensional CRSs may contain an additional $z$ value, typically representing height above sea level).
# 
# In this system, London, for example, can be represented by the coordinates `(-0.1,51.5)`.
# This means that its location is -0.1 degrees east and 51.5 degrees north of the origin.
# The origin, in this case, is at 0 degrees longitude (a prime meridian located at Greenwich) and 0 degrees latitude (the Equator) in a geographic ('lon/lat') CRS (@fig-vector-london, left panel).
# The same point could also be approximated in a projected CRS with 'Easting/Northing' values of `(530000, 180000)` in the British National Grid, meaning that London is located 530 $km$ East and 180 $km$ North of the origin of the CRS (@fig-vector-london, right panel).
# The location of National Grid's origin, in the sea beyond South West Peninsular, ensures that most locations in the UK have positive Easting and Northing values.
# 
# ::: {#fig-vector-london}
# 
# ::: {.columns}
# :::: {.column width="50%"}
# ![](images/vector_lonlat.png)
# ::::
# :::: {.column width="50%"}
# ![](images/vector_projected.png)
# ::::
# :::
# 
# Illustration of vector (point) data in which location of London (the red X) is represented with reference to an origin (the blue circle). 
# The left plot represents a geographic CRS with an origin at 0° longitude and latitude. 
# The right plot represents a projected CRS with an origin located in the sea west of the South West Peninsula.
# :::
# 
# There is more to CRSs, as described in @sec-coordinate-reference-systems-intro and @sec-reproj-geo-data but, for the purposes of this section, it is sufficient to know that coordinates consist of two numbers representing the distance from an origin, usually in $x$ then $y$ dimensions.
# 
# **geopandas** [@geopandas] provides classes for geographic vector data and a consistent command-line interface for reproducible geographic data analysis in Python.
# It also provides an interface to three mature libraries for geocomputation which, in combination, represent a strong foundation on which many geographic applications (including QGIS and R's spatial ecosystem):
# 
# -   GDAL, for reading, writing, and manipulating a wide range of geographic data formats, covered in @sec-read-write
# -   PROJ, a powerful library for coordinate system transformations, which underlies the content covered in @sec-reproj-geo-data
# -   GEOS, a planar geometry engine for operations such as calculating buffers and centroids on data with a projected CRS, covered in @sec-geometric-operations
# 
# Tight integration with these geographic libraries makes reproducible geocomputation possible: an advantage of using a higher level language such as Python to access these libraries is that you do not need to know the intricacies of the low level components, enabling focus on the methods rather than the implementation.
# 
# ### Vector data classes
# 
# The main classes for working with geographic vector data in Python are hierarchical, meaning the highest level 'vector layer' class is composed of simpler 'geometry column' and individual 'geometry' components.
# This section introduces them in order, starting with the highest level class.
# For many applications, the high level vector layer class, which are essentially a data frame with geometry columns, are all that's needed.
# However, it's important to understand the structure of vector geographic objects and their component pieces for more advanced applications.
# The three main vector geographic data classes in Python are:
# 
# -   `GeoDataFrame`, a class representing vector layers, with a geometry column (class `GeoSeries`) as one of the columns
# -   `GeoSeries`, a class that is used to represent the geometry column in `GeoDataFrame` objects
# -   `shapely` geometry objects which represent individual geometries, such as a point or a polygon
# 
# The first two classes (`GeoDataFrame` and `GeoSeries`) are defined in **geopandas**.
# The third class is defined in the **shapely** package, which deals with individual geometries, and is a main dependency of the **geopandas** package.
# 
# ### Vector layers {#sec-vector-layers}
# 
# The most commonly used geographic vector data structure is the vector layer.
# There are several approaches for working with vector layers in Python, ranging from low-level packages (e.g., **osgeo**, **fiona**) to the relatively high-level **geopandas** package that is the focus of this section.
# Before writing and running code for creating and working with geographic vector objects, we need to import **geopandas** (by convention as `gpd` for more concise code) and **shapely**.

# In[ ]:


import pandas as pd
import shapely
import geopandas as gpd


# We also limit the maximum number of printed rows to four, to save space, using the `'display.max_rows'` option of **pandas**.

# In[ ]:


pd.set_option('display.max_rows', 6)


# Projects often start by importing an existing vector layer saved as a GeoPackage (`.gpkg`) file, an ESRI Shapefile (`.shp`), or other geographic file format.
# The function `read_file()` imports a GeoPackage file named `world.gpkg` located in the `data` directory of Python's working directory into a `GeoDataFrame` named `gdf`.

# In[ ]:


#| echo: false
#| label: getdata
from pathlib import Path
import os
import shutil
data_path = Path('data')

if data_path.is_dir():
  pass
  # print('path exists') # directory exists
else:
  print('Attempting to get and unzip the data')
  import requests, zipfile, io
  r = requests.get('https://github.com/geocompx/geocompy/releases/download/0.1/data.zip')
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall('.')

data_path = Path('data/cycle_hire_osm.gpkg')

if data_path.is_file():
  pass
  # print('path exists') # directory exists
else:
  print('Attempting to move data')
  r = requests.get('https://github.com/geocompx/geocompy/archive/refs/heads/main.zip')
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall('.')
  shutil.copytree('py-main/data', 'data', dirs_exist_ok=True) 

data_path = Path('output')

if data_path.is_dir():
  pass
  # print('path exists') # directory exists
else:
  print('Attempting to move data')
  shutil.copytree('py-main/output', 'output', dirs_exist_ok=True) 


# In[ ]:


gdf = gpd.read_file('data/world.gpkg')


# The result is an object of type (class) `GeoDataFrame` with 177 rows (features) and 11 columns, as shown in the output of the following code:

# In[ ]:


#| label: typegdf
type(gdf)


# In[ ]:


gdf.shape


# The `GeoDataFrame` class is an extension of the `DataFrame` class from the popular **pandas** package [@pandas].
# This means we can treat non-spatial attributes from a vector layer as a table, and process them using the ordinary, i.e., non-spatial, established function methods.
# For example, standard data frame subsetting methods can be used.
# The code below creates a subset of the `gdf` dataset containing only the country name and the geometry.

# In[ ]:


gdf = gdf[['name_long', 'geometry']]
gdf


# The following expression creates a subdataset based on a condition, such as equality of the value in the `'name_long'` column to the string `'Egypt'`.

# In[ ]:


gdf[gdf['name_long'] == 'Egypt']


# Finally, to get a sense of the spatial component of the vector layer, it can be plotted using the `.plot` method (@fig-gdf-plot).

# In[ ]:


#| label: fig-gdf-plot
#| fig-cap: Basic plot of a `GeoDataFrame`
gdf.plot();


# Interactive maps of `GeoDataFrame` objects can be created with the `.explore` method, as illustrated in @fig-gdf-explore which was created with the following command:

# In[ ]:


#| label: fig-gdf-explore
#| fig-cap: Basic interactive map with `.explore`
gdf.explore()


# A subset of the data can be also plotted in a similar fashion.

# In[ ]:


#| label: fig-gdf-explore2
#| fig-cap: Interactive map of a `GeoDataFrame` subset
gdf[gdf['name_long'] == 'Egypt'].explore()


# In[ ]:


#| echo: false
# (Alternative)
# import hvplot.pandas
# gdf.hvplot(title='Hello world', geo=True, hover_cols=['name_long'], legend=False).opts(bgcolor='lightgray', active_tools=['wheel_zoom']) 
#This way, we can also add background tiles:
# gdf.hvplot(tiles='OSM', alpha=0.5, geo=True, title='Hello world', hover_cols=['name_long'], legend=False).opts(active_tools=['wheel_zoom']) 


# ### Geometry columns {#sec-geometry-columns}
# 
# The geometry column of class `GeoSeries` is an essential column in a `GeoDataFrame`.
# It contains the geometric part of the vector layer, and is the basis for all spatial operations.
# This column can be accessed by name, which typically (e.g., when reading from a file) is `'geometry'`, as in `gdf['geometry']`.
# However, the recommendation is to use the fixed `.geometry` property, which refers to the geometry column regardless whether its name is `'geometry'` or not.
# In the case of the `gdf` object, the geometry column contains `'MultiPolygon'`s associated with each country.

# In[ ]:


gdf.geometry


# The geometry column also contains the spatial reference information, if any (also accessible with the shortcut `gdf.crs`).

# In[ ]:


gdf.geometry.crs


# Many geometry operations, such as calculating the centroid, buffer, or bounding box of each feature involve just the geometry.
# Applying this type of operation on a `GeoDataFrame` is therefore basically a shortcut to applying it on the `GeoSeries` object in the geometry column.
# For example, the two following commands return exactly the same result, a `GeoSeries` with country bounding box polygons (using the [`.envelope`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.envelope.html) method).

# In[ ]:


gdf.envelope


# In[ ]:


gdf.geometry.envelope


# Note that `.envelope`, and other similar operators in **geopandas** such as `.centroid` (@sec-centroids), `.buffer` (@sec-buffers) or `.convex_hull`, return only the geometry (i.e., a `GeoSeries`), not a `GeoDataFrame` with the original attribute data.
# In case we want the latter, we can create a copy of the `GeoDataFrame` and then "overwrite" its geometry (or, we can overwrite the geometries directly in case we do not need the original ones, as in `gdf.geometry=gdf.envelope`).

# In[ ]:


gdf2 = gdf.copy()
gdf2.geometry = gdf.envelope
gdf2


# Another useful property of the geometry column is the geometry type, as shown in the following code.
# Note that the types of geometries contained in a geometry column (and, thus, a vector layer) are not necessarily the same for every row.
# Accordingly, the `.type` property returns a `Series` (of type `string`), rather than a single value (the same can be done with the shortcut `gdf.geom_type`).

# In[ ]:


gdf.geometry.type


# To summarize the occurrence of different geometry types in a geometry column, we can use the **pandas** method called `value_counts`.

# In[ ]:


gdf.geometry.type.value_counts()


# It is possible to have multiple geometry types in a single `GeoSeries`.
# However, in this case, we see that the `gdf` layer contains only `'MultiPolygon'` geometries.
# 
# A `GeoDataFrame` can also have multiple `GeoSeries`.

# In[ ]:


#| output: false 
gdf['bbox'] = gdf.envelope
gdf['polygon'] = gdf.geometry
gdf


# Only one geometry column at a time is "active", in the sense that it is being accessed in operations involving the geometries (such as `.centroid`, `.crs`, etc.).
# To switch the active geometry column from one `GeoSeries` column to another, we use `set_geometry`.
# @fig-switch-to-centroids and @fig-switch-to-polygons shows interactive maps of the `gdf` layer with the `'bbox'` and `'polygon'` geometry columns activated, respectively.

# In[ ]:


#| label: fig-switch-to-centroids
#| fig-cap: Switching to the `'bbox'` geometry column in the `world` layer, and plotting it
gdf = gdf.set_geometry('bbox')
gdf.explore()


# In[ ]:


#| label: fig-switch-to-polygons
#| fig-cap: Switching to the `'polygons'` geometry column in the `world` layer, and plotting it
gdf = gdf.set_geometry('polygon')
gdf.explore()


# ### The Simple Features standard {#sec-simple-features}
# 
# Geometries are the basic building blocks of vector layers.
# Although the Simple Features standard defines about 20 types of geometries, we will focus on the seven most commonly used types: `POINT`, `LINESTRING`, `POLYGON`, `MULTIPOINT`, `MULTILINESTRING`, `MULTIPOLYGON` and `GEOMETRYCOLLECTION`.
# A useful list of possible geometry types can be found in R's **sf** package [documentation](https://r-spatial.github.io/sf/articles/sf1.html#simple-feature-geometry-types).
# 
# Simple feature geometries can be represented by well-known binary (WKB) and well-known text (WKT) encodings.
# <!-- TODO: add reference or at least link to OGC document on this? --> WKB representations are usually hexadecimal strings easily readable for computers, and this is why GIS software and spatial databases use WKB to transfer and store geometry objects.
# WKT, on the other hand, is a human-readable text markup description of Simple Features.
# <!-- jn: simple features or Simple Features? -->
# <!-- md: Simple Features, now corrected -->
# Both formats are exchangeable, and if we present one, we will naturally choose the WKT representation.
# 
# The foundation of each geometry type is the point.
# A point is simply a coordinate in 2D, 3D, or 4D space such as shown in @fig-point and @fig-point2.
# 
# ``` text
# POINT (5 2)
# ```
# 
# A linestring is a sequence of points with a straight line connecting the points (@fig-linestring).
# 
# ``` text
# LINESTRING (1 5, 4 4, 4 1, 2 2, 3 2)
# ```
# 
# A polygon is a sequence of points that form a closed, non-intersecting ring.
# Closed means that the first and the last point of a polygon have the same coordinates (@fig-polygon).
# 
# ``` text
# POLYGON ((1 5, 2 2, 4 1, 4 4, 1 5))
# ```
# 
# So far we have created geometries with only one geometric entity per feature.
# However, the Simple Features standard allows multiple geometries to exist within a single feature, using "multi" versions of each geometry type, as illustrated in @fig-multipoint, @fig-multilinestring, and @fig-multipolygon1.
# 
# ``` text
# MULTIPOINT (5 2, 1 3, 3 4, 3 2)
# MULTILINESTRING ((1 5, 4 4, 4 1, 2 2, 3 2), (1 2, 2 4))
# MULTIPOLYGON (((1 5, 2 2, 4 1, 4 4, 1 5), (0 2, 1 2, 1 3, 0 3, 0 2)))
# ```
# 
# Finally, a geometry collection can contain any combination of geometries including (multi)points and linestrings (@fig-geometrycollection).
# 
# ``` text
# GEOMETRYCOLLECTION (MULTIPOINT (5 2, 1 3, 3 4, 3 2),
#                     LINESTRING (1 5, 4 4, 4 1, 2 2, 3 2))
# ```
# 
# ### Geometries {#sec-geometries}
# 
# Each element in the geometry column is a geometry object, of class `shapely` [@shapely].
# For example, here is one specific geometry selected by implicit index (Canada, i.e., the 4^th^ element in `gdf`'s geometry column').

# In[ ]:


gdf.geometry.iloc[3]


# We can also select a specific geometry based on the `'name_long'` attribute (i.e., the 1^st^ and only element in the subset of `gdf` where the country name is equal to `Egypt`):

# In[ ]:


gdf[gdf['name_long'] == 'Egypt'].geometry.iloc[0]


# The **shapely** package is compatible with the Simple Features standard (@sec-simple-features).
# Accordingly, seven types of geometry types are supported.
# The following section demonstrates creating a `shapely` geometry of each type from scratch.
# In the first example (a `'Point'`) we show two types of inputs to create a geometry: a list of coordinates or a `string` in the WKT format.
# In the examples for the remaining geometries we use the former approach.
# 
# Creating a `'Point'` geometry from a list of coordinates uses the `shapely.Point` function (@fig-point).

# In[ ]:


#| label: fig-point
#| fig-cap: A `Point` geometry (created from a `list`)
point = shapely.Point([5, 2])
point


# Alternatively, we can use the `shapely.from_wkt` to transform a WKT string to a `shapely` geometry object.
# Here is an example of creating the same `'Point'` geometry from WKT (@fig-point2).

# In[ ]:


#| label: fig-point2
#| fig-cap: A `Point` geometry (created from a WKT string)
point = shapely.from_wkt('POINT (5 2)')
point


# A `'LineString'` geometry can be created based on a list of coordinate tuples or lists (@fig-linestring).

# In[ ]:


#| label: fig-linestring
#| fig-cap: A `LineString` geometry
linestring = shapely.LineString([(1,5), (4,4), (4,1), (2,2), (3,2)])
linestring


# Creation of a `'Polygon'` geometry is similar, but our first and last coordinate must be the same, to ensure that the polygon is closed.
# Note that in the following example, there is one list of coordinates that defines the exterior outer hull of the polygon, followed by a `list` of `list`s of coordinates that define the holes (if any) in the polygon (@fig-polygon).

# In[ ]:


#| label: fig-polygon
#| fig-cap: A `Polygon` geometry
polygon = shapely.Polygon(
    [(1,5), (2,2), (4,1), (4,4), (1,5)],  ## Exterior
    [[(2,4), (3,4), (3,3), (2,3), (2,4)]]  ## Holes
)
polygon


# A `'MultiPoint'` geometry is also created from a list of coordinate tuples (@fig-multipoint), where each element represents a single point.

# In[ ]:


#| label: fig-multipoint
#| fig-cap: A `MultiPoint` geometry
multipoint = shapely.MultiPoint([(5,2), (1,3), (3,4), (3,2)])
multipoint


# A `'MultiLineString'` geometry, on the other hand, has one list of coordinates for each line in the `MultiLineString` (@fig-multilinestring).

# In[ ]:


#| label: fig-multilinestring
#| fig-cap: A `MultiLineString` geometry
multilinestring = shapely.MultiLineString([
    [(1,5), (4,4), (4,1), (2,2), (3,2)],  ## 1st sequence
    [(1,2), (2,4)]  ## 2nd sequence, etc.
])
multilinestring


# A `'MultiPolygon'` geometry (@fig-multipolygon1) is created from a `list` of `Polygon` geometries. For example, here we are creating a `'MultiPolygon'` with two parts, both without holes.

# In[ ]:


#| label: fig-multipolygon1
#| fig-cap: A `MultiPolygon` geometry
multipolygon = shapely.MultiPolygon([
    [[(1,5), (2,2), (4,1), (4,4), (1,5)], []],  ## Polygon 1 
    [[(0,2), (1,2), (1,3), (0,3), (0,2)], []]  ## Polygon 2, etc.
])
multipolygon


# Since the required input has four hierarchical levels, it may be more clear to create the single-part `'Polygon'` geometries in advance, using the respective function (`shapely.Polygon`), and then pass them to `shapely.MultiPolygon` (@fig-multipolygon2). (The same technique can be used with the other `shapely.Multi*` functions.)

# In[ ]:


#| label: fig-multipolygon2
#| fig-cap: A `MultiPolygon` geometry
multipolygon = shapely.MultiPolygon([
    shapely.Polygon([(1,5), (2,2), (4,1), (4,4), (1,5)]),  ## Polygon 1 
    shapely.Polygon([(0,2), (1,2), (1,3), (0,3), (0,2)])  ## Polygon 2, etc.
])
multipolygon


# And, finally, a `'GeometryCollection'` geometry is a `list` with one or more of the other six geometry types (@fig-geometrycollection):

# In[ ]:


#| label: fig-geometrycollection
#| fig-cap: A `GeometryCollection` geometry
geometrycollection = shapely.GeometryCollection([multipoint, multilinestring])
geometrycollection


# `shapely` geometries act as atomic units of vector data, meaning that there is no concept of geometry *sets*: each operation accepts individual geometry object(s) as input, and retunrs an individual geometry as output. (The `GeoSeries` and `GeoDataFrame` objects, defined in **geopandas**, are used to deal with sets of `shapely` geometries, collectively)
# For example, the following expression calculates the difference between the buffered `multipolygon` (using distance of `0.2`) and itself (@fig-mpol-buffer-difference):

# In[ ]:


#| label: fig-mpol-buffer-difference
#| fig-cap: The difference between a buffered `MultiPolygon` and itself
multipolygon.buffer(0.2).difference(multipolygon)


# As demonstrated above, a `shapely` geometry object is automatically evaluated to a small image of the geometry (when using an interface capable of displaying it, such as a Jupyter Notebook).
# To print the WKT string instead, we can use the `print` function:

# In[ ]:


print(linestring)


# Finally, it is important to note that raw coordinates of `shapely` geometries are accessible through a combination of the `.coords`, `.geoms`, `.exterior`, and `.interiors` properties (depending on the geometry type).
# These access methods are helpful when we need to develop our own spatial operators for specific tasks.
# For example, the following expression returns the `list` of all coordinates of the `polygon` geometry exterior:

# In[ ]:


list(polygon.exterior.coords)


# ### Vector layer from scratch {#sec-vector-layer-from-scratch}
# 
# In the previous sections, we started with a vector layer (`GeoDataFrame`), from an existing GeoPackage file, and "decomposed" it to extract the geometry column (`GeoSeries`, @sec-geometry-columns) and separate geometries (`shapely`, see @sec-geometries).
# In this section, we will demonstrate the opposite process, constructing a `GeoDataFrame` from `shapely` geometries, combined into a `GeoSeries`.
# This will help you better understand the structure of a `GeoDataFrame`, and may come in handy when you need to programmatically construct simple vector layers, such as a line between two given points.
# 
# Vector layers consist of two main parts: geometries and non-geographic attributes.
# @fig-gdf-flow shows how a `GeoDataFrame` object is created---geometries come from a `GeoSeries` object (which consists of `shapely` geometries), while attributes are taken from `Series` objects.
# 
# ![Creating a `GeoDataFrame` from scratch](images/gdf-flow.svg){#fig-gdf-flow}
# 
# The final result, a vector layer (`GeoDataFrame`) is therefore a hierarchical structure (@fig-gdf-structure), containing the geometry column (`GeoSeries`), which in turn contains geometries (`shapely`).
# Each of the "internal" components can be accessed, or "extracted", which is sometimes necessary, as we will see later on.
# 
# ![Structure of a `GeoDataFrame`](images/gdf-structure.svg){#fig-gdf-structure}
# 
# Non-geographic attributes may represent the name of the feature, and other attributes such as measured values, groups, etc.
# To illustrate attributes, we will represent a temperature of 25°C in London on June 21st, 2023.
# This example contains a geometry (the coordinates), and three attributes with three different classes (place name, temperature and date).
# Objects of class `GeoDataFrame` represent such data by combining the attributes (`Series`) with the simple feature geometry column (`GeoSeries`).
# First, we create a point geometry, which we know how to do from @sec-geometries (@fig-point-lnd).

# In[ ]:


#| label: fig-point-lnd
#| fig-cap: A `shapely` point representing London
lnd_point = shapely.Point(0.1, 51.5)
lnd_point


# Next, we create a `GeoSeries` (of length 1), containing the point and a CRS definition, in this case WGS84 (defined using its EPSG code `4326`).
# Also note that the `shapely` geometries go into a `list`, to illustrate that there can be more than one geometry unlike in this example.

# In[ ]:


lnd_geom = gpd.GeoSeries([lnd_point], crs=4326)
lnd_geom


# Next, we combine the `GeoSeries` with other attributes into a `dict`.
# The geometry column is a `GeoSeries`, named `geometry`.
# The other attributes (if any) may be defined using `list` or `Series` objects.
# Here, for simplicity, we use the `list` option for defining the three attributes `name`, `temperature`, and `date`.
# Again, note that the `list` can be of length \>1, in case we are creating a layer with more than one feature.

# In[ ]:


lnd_data = {
  'name': ['London'],
  'temperature': [25],
  'date': ['2023-06-21'],
  'geometry': lnd_geom
}


# Finally, the `dict` can be coverted to a `GeoDataFrame` object, as shown in the following code.

# In[ ]:


lnd_layer = gpd.GeoDataFrame(lnd_data)
lnd_layer


# What just happened?
# First, the coordinates were used to create the simple feature geometry (`shapely`).
# Second, the geometry was converted into a simple feature geometry column (`GeoSeries`), with a CRS.
# Third, attributes were combined with `GeoSeries`.
# This results in an `GeoDataFrame` object, named `lnd_layer`.
# 
# To illustrate how does creating a layer with more than one feature looks like, here is an example where we create a layer with two points, London and Paris.

# In[ ]:


lnd_point = shapely.Point(0.1, 51.5)
paris_point = shapely.Point(2.3, 48.9)
towns_geom = gpd.GeoSeries([lnd_point, paris_point], crs=4326)
towns_data = {
  'name': ['London', 'Paris'],
  'temperature': [25, 27],
  'date': ['2013-06-21', '2013-06-21'],
  'geometry': towns_geom
}
towns_layer = gpd.GeoDataFrame(towns_data)
towns_layer


# Now, we are able to create an interactive map of the `towns_layer` object(@fig-layer-from-scratch-explore).
# To make the points easier to see, we are customizing a fill color and size (we elaborate on `.explore` options in @sec-interactive-maps).

# In[ ]:


#| label: fig-layer-from-scratch-explore
#| fig-cap: '`towns_layer`, created from scratch, visualized using `.explore`'
towns_layer.explore(color='red', marker_kwds={'radius': 10})


# Spatial object can be also created from a `pandas.DataFrame` object that contains columns with coordinates.
# For that, we need to first create a `GeoSeries` object from the coordinates, and then combine it with `DataFrame` to a `GeoDataFrame` object.

# In[ ]:


towns_table = pd.DataFrame({
  'name': ['London', 'Paris'],
  'temperature': [25, 27],
  'date': ['2017-06-21', '2017-06-21'],
  'x': [0.1, 2.3],
  'y': [51.5, 48.9]
})
towns_geom = gpd.points_from_xy(towns_table['x'], towns_table['y'])
towns_layer = gpd.GeoDataFrame(towns_table, geometry=towns_geom, crs=4326)


# The output gives the same result as previous `towns_layer`.
# This approach is particularly useful when we need to read data from a CSV file, e.g., using `pandas.read_csv`, and want to turn the resulting `DataFrame` into a `GeoDataFrame` (see another example in @sec-spatial-joining).
# 
# ### Derived numeric properties {#sec-area-length}
# 
# Vector layers are characterized by two essential derived numeric properties: Length (`.length`)---applicable to lines and Area (`.area`)---applicable to polygons.
# Area and length can be calculated for any data structures discussed above, either a `shapely` geometry, in which case the returned value is a number or for `GeoSeries` or `DataFrame`, in which case the returned value is a numeric `Series`.

# In[ ]:


linestring.length


# In[ ]:


multipolygon.area


# In[ ]:


gpd.GeoSeries([point, linestring, polygon, multipolygon]).area


# Like all numeric calculations in **geopandas**, the results assume a planar CRS and are returned in its native units.
# This means that length and area measurements for geometries in WGS84 (`crs=4326`) are returned in decimal degrees and essentially meaningless (to see the warning, try running `gdf.area`).
# 
# To obtain meaningful length and area measurements for data in a geographic CRS, the geometries first need to be transformed to a projected CRS (see @sec-reprojecting-vector-geometries) applicable to the area of interest.
# For example, the area of Slovenia can be calculated in the UTM zone 33N CRS (`crs=32633`).
# The result is in $m^2$, the units of the CRS of this dataset.

# In[ ]:


gdf[gdf['name_long'] == 'Slovenia'].to_crs(32633).area


# ## Raster data {#sec-raster-data}
# 
# The spatial raster data model represents the world with the continuous grid of cells (often also called pixels; @fig-raster-intro-plot1 (A)). 
# This data model often refers to so-called regular grids, in which each cell has the same, constant size---and we will focus on the regular grids in this book only. 
# However, several other types of grids exist, including rotated, sheared, rectilinear, and curvilinear grids (see Chapter 1 of @pebesma_spatial_2022 or Chapter 2 of @tennekes_elegant_2022).
# 
# The raster data model usually consists of a raster header (or metadata) and a matrix (with rows and columns) representing equally spaced cells (often also called pixels; @fig-raster-intro-plot1 (A)). 
# The raster header defines the coordinate reference system, the extent and the origin. 
# The origin (or starting point) is frequently the coordinate of the lower-left corner of the matrix. 
# The metadata defines the extent via the origin, the number of columns, the number of rows, and the cell size resolution. 
# The matrix representation avoids storing explicitly the coordinates for the four corner points (in fact it only stores one coordinate, namely the origin) of each cell, as would be the case for rectangular vector polygons. 
# This and map algebra (@sec-map-algebra) makes raster processing much more efficient and faster than vector data processing. 
# However, in contrast to vector data, the cell of one raster layer can only hold a single value. The value might be numeric or categorical (@fig-raster-intro-plot1 (C)).
# 
# ![Raster data types: (A) cell IDs, (B) cell values, (C) a colored raster map](images/raster-intro-plot1.png){#fig-raster-intro-plot1}
# 
# Raster maps usually represent continuous phenomena such as elevation, temperature, population density or spectral data. 
# Discrete features such as soil or land-cover classes can also be represented in the raster data model. 
# Both uses of raster datasets are illustrated in @fig-raster-intro-plot2, which shows how the borders of discrete features may become blurred in raster datasets. 
# Depending on the nature of the application, vector representations of discrete features may be more suitable.
# 
# ![Examples of continuous and categorical rasters](images/raster-intro-plot2.png){#fig-raster-intro-plot2}
# 
# As mentioned above, working with rasters in Python is less organized around one comprehensive package as compared to the case for vector layers and **geopandas**.
# Instead, several packages provide alternative subsets of methods for working with raster data.
# 
# The two most notable approaches for working with rasters in Python are provided by **rasterio** and **rioxarray** packages.
# As we will see shortly, they differ in scope and underlying data models.
# Specifically, **rasterio** represents rasters as **numpy** arrays associated with a separate object holding the spatial metadata.
# The **rioxarray** package, a warpper of **rasterio**, however, represents rasters with **xarray** "extended" arrays, which are an extension of **numpy** array designed to hold axis labels and attributes in the same object, together with the array of raster values.
# Similar approaches are provided by less well-known **xarray-spatial** and **geowombat** packages.
# Comparatively, **rasterio** is more well-established, but it is more low-level (which has both advantabes and distadvantages).
# 
# All of the above-mentioned packages, however, are not exhaustive in the same way **geopandas** is.
# For example, when working with **rasterio**, on the one hand, more packages may be needed to accomplish common tasks such as zonal statistics (package **rasterstats**) or calculating topographic indices (package **richdem**).
# <!-- On the other hand, **xarray** was extended to accommodate spatial operators missing from the core package itself, with the **rioxarray** and **xarray-spatial** packages. -->
# 
# In the following two sections, we introduce **rasterio**, which is the raster-related package we are going to work with through the rest of the book.
# 
# ### Using **rasterio** {#sec-using-rasterio}
# 
# To work with the **rasterio** package, we first need to import it.
# Additionally, as the raster data is stored within **numpy** arrays, we import the **numpy** package and make all its functions accessible for effective data manipulation. 
# <!-- jn: `rasterio.plot` or **rasterio.plot**?--> 
# <!--md: right! now fixed -->
# Finally, we import the **rasterio.plot** sub-module for its `rasterio.plot.show` function that allows for quick visualization of rasters.
# <!--jn: you should also mention subprocess -->
# <!--md: we didn't actually need it, now removed -->

# In[ ]:


import numpy as np
import rasterio
import rasterio.plot


# Rasters are typically imported from existing files.
# When working with **rasterio**, importing a raster is actually a two-step process:
# 
# -   First, we open a raster file "connection" using `rasterio.open`
# -   Second, we read raster values from the connection using the `.read` method
# 
# This separation is analogous to basic Python functions for reading from files, such as `open` and `.readline` to read from a text file.
# The rationale is that we do not always want to read all information from the file into memory, which is particularly important as rasters size can be larger than RAM size.
# <!-- jn: what do you mean with "selective"? did you mean "optional"? -->
# <!-- md: meaning that we can choose what to read; now rephrased to make it more clear -->
# Accordingly, the second step (`.read`) is selective, meaning that the user can fine tune the subset of values (bands, rows/columns, resolution, etc.) that are actually being read.
# For example, we may want to read just one raster band rather than reading all bands.
# 
# In the first step, we pass a file path to the `rasterio.open` function to create a `DatasetReader` file connection.
# For this example, we use a single-band raster representing elevation in Zion National Park.

# In[ ]:


src = rasterio.open('data/srtm.tif')
src


# To get a first impression of the raster values, we can plot the raster using the `rasterio.plot.show` function (@fig-rasterio-plot):

# In[ ]:


#| label: fig-rasterio-plot
#| fig-cap: Basic plot of a raster, the data are coming from a **rasterio** file connection
rasterio.plot.show(src);


# The `DatasetReader` contains the raster metadata, that is, all of the information other than the raster values.
# Let us examine it with the `meta` property.

# In[ ]:


src.meta


# <!-- jn: maybe it would be good to list and explain the obtained values (e.g., what does the uint16 mean? what does the width? etc.) -->
# <!-- md: agree, now clarified or added references to other places in the book --> 
# Namely, it allows us to see the following properties, which we will elaborate on below, and in later chapters:
# 
# -   `driver`---The raster file format (see @sec-data-output-raster)
# -   `dtype`---Data type (see @tbl-numpy-data-types)
# -   `nodata`---The value being used as "No Data" flag (see @sec-data-output-raster)
# -   Dimensions:
#     - `width`---Number of columns
#     - `height`---Number of rows
#     - `count`---Number of bands
# -   `crs`---Coordinate reference system (see @sec-querying-and-setting-coordinate-systems)
# -   `transform`---The raster affine transformation matrix
# 
# The last item (i.e., `transform`) deserves more attention.
# To position a raster in geographical space, in addition to the CRS, we must specify the raster *origin* ($x_{min}$, $y_{max}$) and resolution ($delta_{x}$, $delta_{y}$).
# In the transformation matrix notation, these data items are stored as follows:
# 
# ```{text}
# Affine(delta_x, 0.0, x_min,
#        0.0, delta_y, y_max)
# ```
# 
# Note that, by convention, raster y-axis origin is set to the maximum value ($y_{max}$) rather than the minimum, and, accordingly, the y-axis resolution ($delta_{y}$) is negative.
# 
# Finally, the `.read` method of the `DatasetReader` is used to read the actual raster values.
# Importantly, we can read:
# 
# -   All layers (as in `.read()`)
# -   A particular layer, passing a numeric index (as in `.read(1)`)
# -   A subset of layers, passing a `list` of indices (as in `.read([1,2])`)
# 
# Note that the layer indices start from `1`, contrary to the Python convention of the first index being `0`.
# 
# The resulting object is a **numpy** array [@numpy], with either two or three dimensions:
# 
# -   *Three* dimensions, when reading more than one layer (e.g., `.read()` or `.read([1,2])`). In such case, the dimensions pattern is `(layers, rows, columns)`
# -   *Two* dimensions, when reading one specific layer (e.g., `.read(1)`). In such case, the dimensions pattern is `(rows, columns)`
# 
# Let's read the first (and only) layer from the `srtm.tif` raster, using the file connection object `src` using the `.read(1)` method.

# In[ ]:


src.read(1)


# The result is a two-dimensional **numpy** array in which each value represents the elevation of the corresponding pixel.
# 
# The relation between a **rasterio** file connection and the derived properties is summarized in @fig-rasterio-structure.
# The file connection (created with `rasterio.open`) gives access to the two components of raster data: the metadata (via the `.meta` property) and the values (via the `.read` method).
# 
# ![Creating a `GeoDataFrame` from scratch](images/rasterio-structure.svg){#fig-rasterio-structure}
# 
# ### Raster from scratch {#sec-raster-from-scratch}
# 
# In this section, we are going to demonstrate the creation of rasters from scratch.
# We will construct two small rasters, `elev` and `grain`, which we will use in examples later in the book.
# Unlike creating a vector layer (see @sec-vector-layer-from-scratch), creating a raster from scratch is rarely needed in practice because aligning a raster with the proper spatial extent is challenging to do programmatically ("georeferencing" tools in GIS software are a better fit for the job).
# Nevertheless, the examples will be helpful to become more familiar with the **rasterio** data structures.
# 
# Conceptually, a raster is an array combined with georeferencing information, whereas the latter comprises:
# 
# -   A transformation matrix, linking pixel indices with coordinates in a particular coordinate system
# -   A CRS definition, specifying the association of that coordinate system with the surface of the earth (optional)
# 
# Therefore, to create a raster, we first need to have an array with the values, and then supplement it with the georeferencing information.
# Let's create the arrays `elev` and `grain`.
# The `elev` array is a $6 \times 6$ array with sequential values from `1` to `36`.
# It can be created as follows using the `np.arange` function and `.reshape` method.
# <!-- jn: why 1, 37, and not 1, 36? -->
# <!-- md: because the 'to' argument is exclusive (like in basic Python's `range`) -->

# In[ ]:


elev = np.arange(1, 37, dtype=np.uint8).reshape(6, 6)
elev


# The `grain` array represents a categorical raster with values `0`, `1`, `2`, corresponding to categories "clay", "silt", "sand", respectively.
# We will create it from a specific arrangement of pixel values using the **numpy** `array` and `reshape` functions.

# In[ ]:


v = [
  1, 0, 1, 2, 2, 2, 
  0, 2, 0, 0, 2, 1, 
  0, 2, 2, 0, 0, 2, 
  0, 0, 1, 1, 1, 1, 
  1, 1, 1, 2, 1, 1, 
  2, 1, 2, 2, 0, 2
]
grain = np.array(v, dtype=np.uint8).reshape(6, 6)
grain


# Note that in both cases, we are using the `uint8` (unsigned integer in 8 bits, i.e., `0-255`) data type, which is sufficient to represent all possible values of the given rasters (see @tbl-numpy-data-types).
# <!-- jn: do we explain possible data types somewhere in the book? if so, we should add a cross-reference here. -->
# <!-- md: yes, good idea! now added -->
# This is the recommended approach for a minimal memory footprint.
# 
# What is missing now is the georeferencing information (see @sec-using-rasterio).
# In this case, since the rasters are arbitrary, we also set up an arbitrary transformation matrix, where:
# 
# -   The origin ($x_{min}$, $y_{max}$) is at `-1.5,1.5`
# -   The raster resolution ($delta_{x}$, $delta_{y}$) is `0.5,-0.5`
# 
# We can add this information using [`rasterio.transform.from_origin`](rasterio.transform.from_origin), and specifying `west`, `north`, `xsize`, and `ysize` parameters.

# In[ ]:


new_transform = rasterio.transform.from_origin(
    west=-1.5, 
    north=1.5, 
    xsize=0.5, 
    ysize=0.5
)
new_transform


# Note that, confusingly, $delta_{y}$ (i.e., `ysize`) is defined in `rasterio.transform.from_origin` using a positive value (`0.5`), even though it is, in fact, negative (`-0.5`).
# 
# The raster can now be plotted in its coordinate system, passing the array `elev` along with the transformation matrix `new_transform` to `rasterio.plot.show` (@fig-rasterio-plot-elev).

# In[ ]:


#| label: fig-rasterio-plot-elev
#| fig-cap: Plot of the `elev` raster, a minimal example of a continuous raster, created from scratch
rasterio.plot.show(elev, transform=new_transform);


# The `grain` raster can be plotted the same way, as we are going to use the same transformation matrix for it as well (@fig-rasterio-plot-grain).

# In[ ]:


#| label: fig-rasterio-plot-grain
#| fig-cap: Plot of the `grain` raster, a minimal example of a categorical raster, created from scratch
rasterio.plot.show(grain, transform=new_transform);


# At this point, we have two rasters, each composed of an array and related transformation matrix.
# We can work with the raster using **rasterio** by:
# 
# -   Passing the transformation matrix wherever actual raster pixel coordinates are important (such as in function `show` above)
# -   Keeping in mind that any other layer we use in the analysis is in the same CRS of those coordinates
# 
# Finally, to export the raster for permanent storage, along with the CRS definition, we need to go through the following steps:
# 
# 1.  Create a raster file connection (where we set the transform and the CRS, among other settings)
# 2.  Write the array with raster values into the connection
# 3.  Close the connection
# 
# Don't worry if the code below is unclear; the concepts related to writing raster data to file will be explained in @sec-data-output-raster. 
# For now, for completeness, and also to use these rasters in subsequent chapters without having to re-create them from scratch, we just provide the code for exporting the `elev` and `grain` rasters into the `output` directory.
# In the case of `elev`, we do it as follows with the `open`, `write`, and `close` methods of the **rasterio** package.
# <!-- jn: please explain 'w', count, crs (add a cross-reference to the section where we explain CRSs) -->
# <!-- md: these are explained in the cited section, now added clarification -->

# In[ ]:


#| eval: false
new_dataset = rasterio.open(
    'output/elev.tif', 'w', 
    driver='GTiff',
    height=elev.shape[0],
    width=elev.shape[1],
    count=1,
    dtype=elev.dtype,
    crs=4326,
    transform=new_transform
)
new_dataset.write(elev, 1)
new_dataset.close()


# Note that the CRS we (arbitrarily) set for the `elev` raster is WGS84, defined using `crs=4326` according to the EPSG code.
# 
# Exporting the `grain` raster is done in the same way, with the only difference being the array we write into the connection.

# In[ ]:


#| eval: false
new_dataset = rasterio.open(
    'output/grain.tif', 'w', 
    driver='GTiff',
    height=grain.shape[0],
    width=grain.shape[1],
    count=1,
    dtype=grain.dtype,
    crs=4326,
    transform=new_transform
)
new_dataset.write(grain, 1)
new_dataset.close()


# As a result, the files `elev.tif` and `grain.tif` are written into the `output` directory.
# We are going to use these small raster files later on in the examples (for example, @sec-raster-subsetting).
# 
# Note that the transform matrices and dimensions of `elev` and `grain` are identical.
# This means that the rasters are overlapping, and can be combined into one two-band raster, processed in raster algebra operations (@sec-map-algebra), etc.
# 
# ## Coordinate Reference Systems {#sec-coordinate-reference-systems-intro}
# 
# Vector and raster spatial data types share concepts intrinsic to spatial data.
# Perhaps the most fundamental of these is the Coordinate Reference System (CRS), which defines how the spatial elements of the data relate to the surface of the Earth (or other bodies).
# CRSs are either geographic or projected, as introduced at the beginning of this chapter (@sec-vector-data).
# This section explains each type, laying the foundations for @sec-reproj-geo-data, which provides a deep dive into setting, transforming, and querying CRSs.
# 
# ### Geographic coordinate systems
# 
# Geographic coordinate systems identify any location on the Earth's surface using two values---longitude and latitude (see left panel of @fig-zion-crs).
# Longitude is a location in the East-West direction in angular distance from the Prime Meridian plane, while latitude is an angular distance North or South of the equatorial plane.
# Distances in geographic CRSs are therefore not measured in meters.
# This has important consequences, as demonstrated in @sec-reproj-geo-data.
# 
# A spherical or ellipsoidal surface represents the surface of the Earth in geographic coordinate systems.
# Spherical models assume that the Earth is a perfect sphere of a given radius---they have the advantage of simplicity, but, at the same time, they are inaccurate: the Earth is not a sphere!
# Ellipsoidal models are defined by two parameters: the equatorial radius and the polar radius.
# These are suitable because the Earth is compressed: the equatorial radius is around 11.5 $km$ longer than the polar radius.
# <!-- TODO: add reference, (Maling 1992...). -->
# The Earth is not an ellipsoid either, but it is a better approximation than a sphere.
# 
# Ellipsoids are part of a broader component of CRSs: the datum.
# It contains information on what ellipsoid to use and the precise relationship between the Cartesian coordinates and location on the Earth's surface.
# There are two types of datum---geocentric (such as WGS84) and local (such as NAD83).
# You can see examples of these two types of datums in @fig-geocentric-vs-local.
# Black lines represent a geocentric datum, whose center is located in the Earth's center of gravity and is not optimized for a specific location.
# In a local datum, shown as a purple dashed line, the ellipsoidal surface is shifted to align with the surface at a particular location.
# These allow local variations on Earth's surface, such as large mountain ranges, to be accounted for in a local CRS.
# This can be seen in @fig-geocentric-vs-local, where the local datum is fitted to the area of Philippines, but is misaligned with most of the rest of the planet's surface.
# Both datums in @fig-geocentric-vs-local are put on top of a geoid---a model of global mean sea level.
# 
# ![Geocentric and local geodetic datums shown on top of a geoid (in false color and the vertical exaggeration by 10,000 scale factor). Image of the geoid is adapted from the work of [@essd-11-647-2019].](https://r.geocompx.org/figures/02_datum_fig.png){#fig-geocentric-vs-local}
# 
# ### Projected coordinate reference systems {#sec-projected-coordinate-reference-systems}
# 
# All projected CRSs are based on a geographic CRS, described in the previous section, and rely on map projections to convert the three-dimensional surface of the Earth into Easting and Northing (x and y) values in a projected CRS.
# Projected CRSs are based on Cartesian coordinates on an implicitly flat surface (see right panel of @fig-zion-crs).
# They have an origin, x and y axes, and a linear unit of measurement such as meters.
# 
# This transition cannot be done without adding some deformations.
# Therefore, some properties of the Earth's surface are distorted in this process, such as area, direction, distance, and shape.
# A projected coordinate system can preserve only one or two of those properties.
# Projections are often named based on a property they preserve: equal-area preserves area, azimuthal preserves direction, equidistant preserves distance, and conformal preserves local shape.
# 
# There are three main groups of projection types: conic, cylindrical, and planar (azimuthal).
# In a conic projection, the Earth's surface is projected onto a cone along a single line of tangency or two lines of tangency.
# Distortions are minimized along the tangency lines and rise with the distance from those lines in this projection.
# Therefore, it is best suited for maps of mid-latitude areas.
# A cylindrical projection maps the surface onto a cylinder.
# This projection could also be created by touching the Earth's surface along a single line of tangency or two lines of tangency.
# Cylindrical projections are used most often when mapping the entire world.
# A planar projection projects data onto a flat surface touching the globe at a point or along a line of tangency.
# It is typically used in mapping polar regions.
# 
# ### CRS in Python {#sec-crs-python}
# 
# Like most open-source geospatial software, the **geopandas** and **rasterio** packages use the PROJ software for CRS definition and calculations.
# The **pyproj** package is a low-level interface to PROJ.
# Using its functions, such as `get_codes` and `from_epsg`, we can examine the list of projections supported by PROJ.

# In[ ]:


import pyproj
epsg_codes = pyproj.get_codes('EPSG', 'CRS')  ## Supported EPSG codes
epsg_codes[:5]  ## Print first five supported EPSG codes


# In[ ]:


pyproj.CRS.from_epsg(4326)  ## Printout of WGS84 CRS (EPSG:4326)


# A quick summary of different projections, their types, properties, and suitability can be found in "Map Projections" (1993) and at <https://www.geo-projections.com/>.
# We will expand on CRSs and explain how to project from one CRS to another in @sec-reproj-geo-data.
# But, for now, it is sufficient to know:
# 
# -   That coordinate systems are a key component of geographic objects
# -   Knowing which CRS your data is in, and whether it is in geographic (lon/lat) or projected (typically meters), is important and has consequences for how Python handles spatial and geometry operations
# -   CRSs of **geopandas** (vector layer or geometry column) and **rasterio** (raster) objects can be queried with the `.crs` property
# 
# Here is a demonstration of the last bullet point, where we import a vector layer and figure out its CRS (in this case, a projected CRS, namely UTM Zone 12) using the `.crs` property.

# In[ ]:


zion = gpd.read_file('data/zion.gpkg')
zion.crs


# We can also illustrate the difference between a geographic and a projected CRS by plotting the `zion` data in both CRSs (@fig-zion-crs). Note that we are using the [`.grid`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.grid.html) method of **matplotlib** to draw grid lines on top of the plot.
# <!-- jn: have we explained the grid() method first? if not, we should do it here. -->
# <!-- md: now added reference -->
# <!-- jn: the plot does not align well (1e6 number above the right panel)... -->
# <!-- md: not sure I understand, the 1e6 is a factor automatically added to keep the axis labels as small numbers -->

# In[ ]:


#| label: fig-zion-crs
#| fig-cap: Examples of Coordinate Refrence Systems (CRS) for a vector layer 
#| fig-subcap: 
#| - Geographic (WGS84)
#| - Projected (NAD83 / UTM zone 12N)
#| layout-ncol: 2
# WGS84
zion.to_crs(4326).plot(edgecolor='black', color='lightgrey').grid()
# NAD83 / UTM zone 12N
zion.plot(edgecolor='black', color='lightgrey').grid();


# We are going to elaborate on reprojection from one CRS to another (`.to_crs` in the above code section) in @sec-reproj-geo-data.
# 
# ## Units
# 
# An important feature of CRSs is that they contain information about spatial units.
# Clearly, it is vital to know whether a house's measurements are in feet or meters, and the same applies to maps.
# It is a good cartographic practice to add a scale bar or some other distance indicator onto maps to demonstrate the relationship between distances on the page or screen and distances on the ground.
# Likewise, it is important for the user to be aware of the units in which the geometry coordinates are, to ensure that subsequent calculations are done in the right context.
# 
# Python spatial data structures in **geopandas** and **rasterio** do not natively support the concept of measurement units.
# The coordinates of a vector layer or a raster are plain numbers, referring to an arbitrary plane.
# For example, according to the `.transform` matrix of `srtm.tif` we can see that the raster resolution is `0.000833` and that its CRS is WGS84 (EPSG: `4326`):

# In[ ]:


src.meta


# You may already know that the units of the WGS84 coordinate system (EPSG:4326) are decimal degrees.
# However, that information is not accounted for in any numeric calculation, meaning that operations such as buffers can be returned in units of degrees, which is not appropriate in most cases.
# 
# Consequently, you should always be aware of the CRS of your datasets and the units they use.
# Typically, these are decimal degrees, in a geographic CRS, or $m$, in a projected CRS, although there are exceptions.
# Geometric calculations such as length, area, or distance, return plain numbers in the same units of the CRS (such as $m$ or $m^2$).
# It is up to the user to determine which units the result is given in, and treat the result accordingly.
# For example, if the area output was in $m^2$ and we need the result in $km^2$, then we need to divide the result by $1000^2$.
# 
# ## Exercises
# 
# ## References
