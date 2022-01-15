# (PART) Foundations {-}

# Geographic data in Python {#spatial-class}

## Prerequisites

* Python basics: basic data types, assignment, loops, function calls and definition
* `numpy`: creating arrays, array data types, array reshaping, subsetting, assignment to subsets, vectorized operations, no-data values, masking and assignment
* `pandas`: creating `Series` (vectors) and `DataFrame` (tables), indexes, subsetting, assignment to subsets, calculating new columns, sorting, filtering, renaming columns, aggregation, join, reading and writing

## Introduction

...

## Vector data

### Geometries

...

### Geometry columns

...

### Vector layers

...


## Raster data

...

## Coordinate Reference Systems

...

## Units

...

## Exercises

...


```python
import matplotlib.pyplot as plt
import geopandas
from cartopy import crs as ccrs

path = geopandas.datasets.get_path('naturalearth_lowres')
df = geopandas.read_file(path)
# Add a column we'll use later
df['gdp_pp'] = df['gdp_md_est'] / df['pop_est']
df.plot()
```

<img src="02-spatial-data_files/figure-html/unnamed-chunk-1-1.png" width="672" />

