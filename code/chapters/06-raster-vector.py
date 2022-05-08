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

# # Raster-vector interactions {#raster-vector}
#
# ## Prerequisites

#| echo: false
import pandas as pd
import matplotlib.pyplot as plt
pd.options.display.max_rows = 6
pd.options.display.max_columns = 6
pd.options.display.max_colwidth = 35
plt.rcParams["figure.figsize"] = (5, 5)

# Let's import the required packages:

import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import rasterio.mask
from rasterio.plot import show

# and load the sample data:

src_srtm = rasterio.open("data/srtm.tif")
zion = gpd.read_file("data/zion.gpkg")
zion_points = gpd.read_file("data/zion_points.gpkg")

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
    zion["geometry"], 
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

new_dataset = rasterio.open("output/srtm_masked.tif", "w", **out_meta)
new_dataset.write(out_image_mask)
new_dataset.close()

# Now we can re-import the raster:

src_srtm_mask = rasterio.open("output/srtm_masked.tif")

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

# Figure ... shows the original raster, and the cropped and masked results.

fig, axes = plt.subplots(ncols=3, figsize=(9,5))
show(src_srtm, ax=axes[0])
zion.plot(ax=axes[0], color="none", edgecolor="black")
show(src_srtm_mask, ax=axes[1])
zion.plot(ax=axes[1], color="none", edgecolor="black")
show(out_image_crop, transform=out_transform_crop, ax=axes[2])
zion.plot(ax=axes[2], color="none", edgecolor="black")
axes[0].set_title("Original")
axes[1].set_title("Mask")
axes[2].set_title("Crop");

# ## Raster extraction
#
# From points...
#
# From line...
#
# From polygon (srtm)...
#
# From polygon (nlcd)...
#
# ## Rasterization
#
# ## Spatial vectorization

src = rasterio.open("data/grain.tif")

# ## Exercises
