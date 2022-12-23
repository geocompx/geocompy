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

# # Raster-vector interactions {#raster-vector}
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
import shapely.geometry
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import rasterio.mask
import rasterstats
from rasterio.plot import show
import math

# and load the sample data:

src_srtm = rasterio.open('data/srtm.tif')
src_nlcd = rasterio.open('data/nlcd.tif')
src_grain = rasterio.open('data/grain.tif')
src_elev = rasterio.open('data/elev.tif')
zion = gpd.read_file('data/zion.gpkg')
zion_points = gpd.read_file('data/zion_points.gpkg')
cycle_hire_osm = gpd.read_file('data/cycle_hire_osm.gpkg')

# ## Introduction
#
# ## Raster cropping
#
# Many geographic data projects involve integrating data from many different sources, such as remote sensing images (rasters) and administrative boundaries (vectors). Often the extent of input raster datasets is larger than the area of interest. In this case raster **cropping** and **masking** are useful for unifying the spatial extent of input data. Both operations reduce object memory use and associated computational resources for subsequent analysis steps, and may be a necessary preprocessing step before creating attractive maps involving raster data.
#
# We will use two objects to illustrate raster cropping:
#
# * The `srtm.tif` raster representing elevation (meters above sea level) in south-western Utah
# * The `zion.gpkg` vector layer representing the Zion National Park
#
# Both target and cropping objects must have the same projection. The following reprojects the vector layer `zion` into the CRS of the raster `src_srtm`:

zion = zion.to_crs(src_srtm.crs)

# To mask the image, i.e., convert all pixels which do not intersect with the `zion` polygon to "No Data", we use the `rasterio.mask.mask` function as follows:

out_image_mask, out_transform_mask = rasterio.mask.mask(
    src_srtm, 
    zion['geometry'], 
    crop=False, 
    nodata=9999
)

# Note that we need to specify a "No Data" value in agreement with the raster data type. Since `srtm.tif` is of type `uint16`, we choose `9999` (a positive integer that is guaranteed not to occur in the raster). 
#
# The result is the `out_image` array with the masked values: 

out_image_mask

# and the new `out_transform`:

out_transform_mask

# Note that masking (without cropping!) does not modify the raster spatial configuration. Therefore, the new transform is identical to the original:

src_srtm.transform

# Unfortunately, the `out_image` and `out_transform` object do not contain any information indicating that `9999` represents "No Data". To associate the information with the raster, we must write it to file along with the corresponding metadata. For example, to write the cropped raster to file, we need to modify the "No Data" setting in the metadata:

out_meta = src_srtm.meta
out_meta.update(nodata=9999)
out_meta

# Then we can write the cropped raster to file:

new_dataset = rasterio.open('output/srtm_masked.tif', 'w', **out_meta)
new_dataset.write(out_image_mask)
new_dataset.close()

# Now we can re-import the raster:

src_srtm_mask = rasterio.open('output/srtm_masked.tif')

# The `.meta` property contains the `nodata` entry. Now, any relevant operation (such as plotting) will take "No Data" into account:

src_srtm_mask.meta

# Cropping means reducing the raster extent to the extent of the vector layer:
#
# * To crop *and* mask, we can use the same in `rasterio.mask.mask` expression shown above for masking, just setting `crop=True` instead of `crop=False`. 
# * To just crop, *without* masking, we can derive the extent polygon and then crop using it.
#
# For example, here is how we can obtain the extent polygon of `zion`, as a `shapely` geometry object:

bb = zion.unary_union.envelope
bb

# The extent can now be used for masking. Here, we are also using the `all_touched=True` option so that pixels partially overlapping with the extent are included:

out_image_crop, out_transform_crop = rasterio.mask.mask(
    src_srtm, 
    [bb], 
    crop=True, 
    all_touched=True, 
    nodata=9999
)

# @fig-raster-crop shows the original raster, and the cropped and masked results.

# +
#| label: fig-raster-crop
#| fig-cap: Raster masking and cropping

fig, axes = plt.subplots(ncols=3, figsize=(9,5))
show(src_srtm, ax=axes[0])
zion.plot(ax=axes[0], color='none', edgecolor='black')
show(src_srtm_mask, ax=axes[1])
zion.plot(ax=axes[1], color='none', edgecolor='black')
show(out_image_crop, transform=out_transform_crop, ax=axes[2])
zion.plot(ax=axes[2], color='none', edgecolor='black')
axes[0].set_title('Original')
axes[1].set_title('Mask')
axes[2].set_title('Crop');
# -

# ## Raster extraction
#
# Raster extraction is the process of identifying and returning the values associated with a 'target' raster at specific locations, based on a (typically vector) geographic 'selector' object. The reverse of raster extraction — assigning raster cell values based on vector objects — is rasterization, described in Section ...
#
# In the following examples, we use a third-party package called `rasterstats`, which is specifically aimed at extracting raster values: 
#
# * to *points*, via the `rasterstats.point_query` function, or 
# * to *polygons*, via the `rasterstats.zonal_stats` function.
#
# ### Extraction to points
#
# The basic example is of extracting the value of a raster cell at specific points. For this purpose, we will use `zion_points`, which contain a sample of 30 locations within the Zion National Park (Figure ...). The following expression extracts elevation values from `srtm`:

result = rasterstats.point_query(
    zion_points, 
    src_srtm.read(1), 
    nodata = src_srtm.nodata, 
    affine = src_srtm.transform,
    interpolate='nearest'
)

# The resulting object is a `list` of raster values, corresponding to `zion_points`:

result[:5]

# To create a `DataFrame` with points' IDs (one value per vector's row) and related `srtm` values for each point, we need to assign it:

zion_points['elev'] = result
zion_points

# ### Extraction to lines
#
# Raster extraction also works with line selectors. Then, it extracts one value for each raster cell touched by a line. However, the line extraction approach is not recommended to obtain values along the transects as it is hard to get the correct distance between each pair of extracted raster values.
#
# In this case, a better approach is to split the line into many points and then extract the values for these points. To demonstrate this, the code below creates zion_transect, a straight line going from northwest to southeast of the Zion National Park, illustrated in Figure 6.3(A) (see Section 2.2 for a recap on the vector data model):
#
# zion_transect = cbind(c(-113.2, -112.9), c(37.45, 37.2)) |>
#   st_linestring() |> 
#   st_sfc(crs = crs(srtm)) |>
#   st_sf(geometry = _)
#
# The utility of extracting heights from a linear selector is illustrated by imagining that you are planning a hike. The method demonstrated below provides an ‘elevation profile’ of the route (the line does not need to be straight), useful for estimating how long it will take due to long climbs.
#
# The first step is to add a unique id for each transect. Next, with the st_segmentize() function we can add points along our line(s) with a provided density (dfMaxLength) and convert them into points with st_cast().
#
# zion_transect$id = 1:nrow(zion_transect)
# zion_transect = st_segmentize(zion_transect, dfMaxLength = 250)
# zion_transect = st_cast(zion_transect, "POINT")
#
# Now, we have a large set of points, and we want to derive a distance between the first point in our transects and each of the subsequent points. In this case, we only have one transect, but the code, in principle, should work on any number of transects:
#
# zion_transect = zion_transect |> 
#   group_by(id) |> 
#   mutate(dist = st_distance(geometry)[, 1]) 
#
# Finally, we can extract elevation values for each point in our transects and combine this information with our main object.
#
# zion_elev = terra::extract(srtm, vect(zion_transect))
# zion_transect = cbind(zion_transect, zion_elev)
#
# The resulting zion_transect can be used to create elevation profiles, as illustrated in Figure 6.3(B).
#
# ### Extraction to polygons
#
# The final type of geographic vector object for raster extraction is polygons. Like lines, polygons tend to return many raster values per polygon. Typically, we generate summary statistics for raster values per polygon, for example to characterize a single region or to compare many regions. The generation of raster summary statistics, by polygons, is demonstrated in the code below, which creates a list of summary statistics (in this case a list of length 1, since there is just one polygon), again using `rasterstats`:

rasterstats.zonal_stats(
    zion, 
    src_srtm.read(1), 
    nodata = src_srtm.nodata, 
    affine = src_srtm.transform, 
    stats = ['mean', 'min', 'max']
)

# The results provide useful summaries, for example that the maximum height in the park is around 2,661 meters above see level (other summary statistics, such as standard deviation, can also be calculated in this way). Because there is only one polygon in the example a data frame with a single row is returned; however, the method works when multiple selector polygons are used.
#
# Note the `stats` argument, where we determine what type of statistics are calculated per polygon. Possible values other than `'mean'`, `'min'`, `'max'` are:
#
# * `'count'`—The number of valid (i.e., excluding "No Data") pixels
# * `'nodata'`—The number of pixels with 'No Data"
# * `'majority'`—The most frequently occurring value
# * `'median'`—The median value
#
# See the [documentation](https://pythonhosted.org/rasterstats/manual.html#statistics) for the complete list. Additionally, the `zonal_stats` function accepts user-defined functions for calculating any custom statistics.
#
# To count occurrences of categorical raster values within polygons, we can use masking (see Section...) combined with `np.unique`, as follows:

out_image, out_transform = rasterio.mask.mask(
    src_nlcd, 
    zion['geometry'].to_crs(src_nlcd.crs), 
    crop=False, 
    nodata=9999
)
counts = np.unique(out_image, return_counts=True)

# According to the result, for example, pixel value `2` ("Developed" class) appears in `4205` pixels within the Zion polygon:

counts

# Raster to polygon extraction is illustrated in @fig-raster-extract-to-polygon.

# +
#| label: fig-raster-extract-to-polygon
#| fig-cap: Area used for continuous (left) and categorical (right) raster extraction.

fig, axes = plt.subplots(ncols=2, figsize=(6,4))
show(src_srtm, ax=axes[0])
zion.plot(ax=axes[0], color='none', edgecolor='black')
show(src_nlcd, ax=axes[1], cmap='Set3')
zion.to_crs(src_nlcd.crs).plot(ax=axes[1], color='none', edgecolor='black')
axes[0].set_title('Continuous data extraction')
axes[1].set_title('Categorical data extraction');
# -

# ## Rasterization
#
# Rasterization is the conversion of vector objects into their representation in raster objects. Usually, the output raster is used for quantitative analysis (e.g., analysis of terrain) or modeling. As we saw in Chapter 2 the raster data model has some characteristics that make it conducive to certain methods. Furthermore, the process of rasterization can help simplify datasets because the resulting values all have the same spatial resolution: rasterization can be seen as a special type of geographic data aggregation.
#
# The `rasterio` package contains the `rasterio.features.rasterize` function for doing this work. To make it happen, we need to have the "template" grid definition, i.e., the "template" raster defining the extent, resolution and CRS of the output, in the form of `out_shape` (the dimensions) and `transform` (the transform). In case we have an existing template raster, we simply need to query its `out_shape` and `transform`. In case we create a custom template, e.g., covering the vector layer extent with specified resolution, there is some extra work to calculate the `out_shape` and `transform` (see next example). 
#
# Furthermore, the `rasterio.features.rasterize` function requires the input shapes in the form for a generator of `(geom, value)` tuples, where:
#
# * `geom` is the given geometry (`shapely`)
# * `value` is the value to be "burned" into pixels coinciding with the geometry (`int` or `float`)
#
# Again, this will be made clear in the next example.
#
# The geographic resolution of the "template" raster has a major impact on the results: if it is too low (cell size is too large), the result may miss the full geographic variability of the vector data; if it is too high, computational times may be excessive. There are no simple rules to follow when deciding an appropriate geographic resolution, which is heavily dependent on the intended use of the results. Often the target resolution is imposed on the user, for example when the output of rasterization needs to be aligned to the existing raster.
#
# To demonstrate rasterization in action, we will use a template raster that has the same extent and CRS as the input vector data `cycle_hire_osm_projected` (a dataset on cycle hire points in London is illustrated in @fig-rasterize-points) and spatial resolution of 1000 meters. First, we obtain the vector layer:

cycle_hire_osm_projected = cycle_hire_osm.to_crs(27700)
cycle_hire_osm_projected

# Next, we need to calculate the `out_shape` and `transform` of out template raster. To calculate the transform, we combine the top-left corner of the `cycle_hire_osm_projected` bounding box with the required resolution (e.g., 1000 $m$):

bounds = cycle_hire_osm_projected.total_bounds
bounds

res = 1000
transform = rasterio.transform.from_origin(
    west=bounds[0], 
    north=bounds[3], 
    xsize=res, 
    ysize=res
)
transform

# To calculate the `out_shape`, we divide the x-axis and y-axis extent by the resolution:

rows = math.ceil((bounds[3] - bounds[1]) / res)
cols = math.ceil((bounds[2] - bounds[0]) / res)
shape = (rows, cols)
shape

# Now, we can rasterize. Rasterization is a very flexible operation: the results depend not only on the nature of the template raster, but also on the type of input vector (e.g., points, polygons), the pixel "activation" method, and the function applied when there is more than one match.
#
# To illustrate this flexibility we will try three different approaches to rasterization. First, we create a raster representing the presence or absence of cycle hire points (known as presence/absence rasters). In this case, we transfer the value of `1` to all pixels where at least one point falls in. To transform the point `GeoDataFrame` into a generator of `shapely` geometries and the (fixed) values, we use the following expression:

((g, 1) for g in cycle_hire_osm_projected['geometry'].to_list())

# Therefore, the rasterizing expression is:

ch_raster1 = rasterio.features.rasterize(
    ((g, 1) for g in cycle_hire_osm_projected['geometry'].to_list()),
    out_shape=shape,
    transform=transform
)

# The result is a `numpy` array with the burned values of `1`, and `0` in unaffected "pixels":

ch_raster1

# To count the number of stations, we can use the fixed value of `1` combined with the `merge_alg=rasterio.enums.MergeAlg.add`, which means that multiple values burned into the same pixel are *summed*, rather than replaced keeping last (the default):

ch_raster2 = rasterio.features.rasterize(
    ((g, 1) for g in cycle_hire_osm_projected['geometry'].to_list()),
    out_shape=shape,
    transform=transform,
    merge_alg=rasterio.enums.MergeAlg.add
)

# Here is the resulting array of counts:

ch_raster2

# The new output, `ch_raster2`, shows the number of cycle hire points in each grid cell. The cycle hire locations have different numbers of bicycles described by the capacity variable, raising the question, what's the capacity in each grid cell? To calculate that, we must sum the field (`"capacity"`) rather than the fixed values of `1`. This requires using an expanded generator of geometries and values, where we (1) extract both geometries and attribute values, and (2) filter out "No Data" values, as follows:

ch_raster3 = rasterio.features.rasterize(
    ((g, v) for g, v in cycle_hire_osm_projected[['geometry', 'capacity']] \
        .dropna(subset='capacity')
        .to_numpy() \
        .tolist()),
    out_shape=shape,
    transform=transform,
    merge_alg=rasterio.enums.MergeAlg.add
)

# Here is the code to illustrate the input point layer `cycle_hire_osm_projected` and the three variants of rasterizing it `ch_raster1`, `ch_raster2`, and `ch_raster3` (@fig-rasterize-points):

# +
#| label: fig-rasterize-points
#| fig-cap: Examples of point rasterization.

fig, axes = plt.subplots(2, 2, figsize=(9, 9))
cycle_hire_osm_projected.plot(ax=axes[0][0], column='capacity')
show(ch_raster1, transform=transform, ax=axes[0][1])
show(ch_raster2, transform=transform, ax=axes[1][0])
show(ch_raster3, transform=transform, ax=axes[1][1])
axes[0][0].set_title('Points')
axes[0][1].set_title('Presence/Absence')
axes[1][0].set_title('Count')
axes[1][1].set_title('Aggregated capacity');
# -

# ## Spatial vectorization
#
# Spatial vectorization is the counterpart of rasterization (Section ...), but in the opposite direction. It involves converting spatially continuous raster data into spatially discrete vector data such as points, lines or polygons.
#
# There are three standard methods to convert a raster to a vector layer:
#
# * Raster to polygons
# * Raster to points
# * Raster to contours
#
# The most straightforward form of vectorization is the first one, converting raster cells to polygons, where each pixel is represented by a rectangular polygon. The second method, raster to points, has the additional step of calculating polygon centroids. The third method, raster to contours, is somewhat unrelated. Let us demonstrate the three in the given order.
#
# The `rasterio.features.shapes` function can be used to access to the raster pixel as polygon geometries, as well as raster values. The returned object is a generator, which yields `geometry,value` pairs. The additional `transform` argument is used to yield true spatial coordinates of the polygons, which is usually what we want. 
#
# For example, the following expression returns a generator named `shapes`, referring to the pixel polygons:

shapes = rasterio.features.shapes(src_grain.read(), transform=src_grain.transform)
shapes

# We can generate all shapes at once, into a `list` named `pol`, as follows:

pol = list(shapes)

# Each element in `pol` is a `tuple` of length 2, containing:
#
# * The GeoJSON-like `dict` representing the polygon geometry
# * The value of the pixel(s) which comprise the polygon
#
# For example:

pol[0]

# Note that each raster cell is converted into a polygon consisting of five coordinates, all of which are stored in memory (explaining why rasters are often fast compared with vectors!).
#
# To transform the `list` into a `GeoDataFrame`, we need few more steps of data reshaping:

# Create 'GeoSeries' with the polygons
geom = [shapely.geometry.shape(i[0]) for i in pol]
geom = gpd.GeoSeries(geom, crs=src_grain.crs)
# Create 'Series' with the values
values = [i[1] for i in pol]
values = pd.Series(values)
# Combine the 'Series' and 'GeoSeries' into a 'DataFrame'
result = gpd.GeoDataFrame({'value': values, 'geometry': geom})
result

# The resulting polygon layer is shown in @fig-raster-to-polygons. As shown using the `edgecolor='black'` option, neighboring pixels sharing the same raster value are dissolved into larger polygons. The `rasterio.features.shapes` function does not offer a way to avoid this type of dissolving. One way to work around that is to convert an array with consecutive IDs, instead of the real values, to polygons, then extract the real values from the raster (similarly to the "raster to points" example, see below).

# +
#| label: fig-raster-to-polygons
#| fig-cap: grain.tif converted to polygon layer

result.plot(column='value', edgecolor='black', legend=True);
# -

# To transform raster to points, we can use `rasterio.features.shapes`, as in conversion to polygons, only with the addition of the `.centroid` method to go from polygons to their centroids. However, to avoid dissolving nearby pixels, we will actually convert a raster with consecutive IDs, then extract the "true" values by point (it is not strictly necessary in this example, since the values of `elev.tif` are all unique):

# Prepare IDs array
r = src_elev.read(1)
ids = r.copy()
ids = np.arange(0, r.size).reshape(r.shape).astype(np.int32)
ids

# IDs raster to points
shapes = rasterio.features.shapes(ids, transform=src_elev.transform)
pol = list(shapes)
geom = [shapely.geometry.shape(i[0]).centroid for i in pol]
geom = gpd.GeoSeries(geom, crs=src_elev.crs)
result = gpd.GeoDataFrame(geometry=geom)

# Extract values to points
result['value'] = rasterstats.point_query(
    result, 
    r, 
    nodata = src_elev.nodata, 
    affine = src_elev.transform,
    interpolate='nearest'
)

# The result is shown in @fig-raster-to-points.

# +
#| label: fig-raster-to-points
#| fig-cap: Raster and point representation of the `elev.tif`.

fig, axes = plt.subplots(1, 2, figsize=(8, 4))
result.plot(column='value', legend=True, ax=axes[0]);
show(src_elev, transform=src_elev.transform, ax=axes[0])
result.plot(column='value', legend=True, ax=axes[1]);
show(src_elev, cmap='Greys', ax=axes[1]);
# -

# To contours...
#
# ...
#
# Another common type of spatial vectorization is the creation of contour lines representing lines of continuous height or temperatures (isotherms) for example. We will use a real-world digital elevation model (DEM) because the artificial raster elev produces parallel lines (task for the reader: verify this and explain why this happens). Contour lines can be created with the terra function as.contour(), which is itself a wrapper around filled.contour(), as demonstrated below (not shown):
#
# Contours can also be added to existing plots with functions such as contour(), rasterVis::contourplot() or tmap::tm_iso(). As illustrated in Figure 6.8, isolines can be labelled.
#
# The final type of vectorization involves conversion of rasters to polygons. This can be done with terra::as.polygons(), which converts each raster cell into a polygon consisting of five coordinates, all of which are stored in memory (explaining why rasters are often fast compared with vectors!).
#
# This is illustrated below by converting the grain object into polygons and subsequently dissolving borders between polygons with the same attribute values (also see the dissolve argument in as.polygons()).
#
#
#
# ## Exercises
#
