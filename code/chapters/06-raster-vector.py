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

# # Raster-vector interactions {#raster-vector}
#
# ## Introduction

import numpy as np
import geopandas as gpd
import rasterio
import rasterio.mask
from rasterio.plot import show

# ## Raster cropping

src = rasterio.open("data/srtm.tif")

pol = gpd.read_file("data/zion.gpkg")

pol = pol.to_crs(src.crs)

out_image, out_transform = rasterio.mask.mask(src, pol.geometry, crop = False, nodata = 9999)

show(out_image)

meta = src.meta
meta.update(height = out_image[0].shape[0])
meta.update(width = out_image[0].shape[1])
meta.update(transform = out_transform)
meta.update(nodata = 9999)
meta

new_dataset = rasterio.open("output/srtm_cropped.tif", "w", **meta)
new_dataset.write(out_image)
new_dataset.close()

src2 = rasterio.open("output/srtm_cropped.tif")
show(src2)

src2.meta

src2.read()

# Plot...

fig, axes = plt.subplots(ncols=3, figsize=(15,5))
show(src, ax=axes[0])
show(src2, ax=axes[2])
axes[0].set_title("Original")
axes[1].set_title("Crop")
axes[2].set_title("Mask");

# ## Raster extraction
#
# ## Rasterization
#
# ## Spatial vectorization

src = rasterio.open("data/grain.tif")

# ## Exercises
