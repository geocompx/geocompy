# (PART) Foundations {-}

# Geographic data in Python {#spatial-class}

## Introduction

...

Importing packages


```python
import shapely.geometry
import geopandas as gpd
```


```python
# import matplotlib.pyplot as plt
```

## Vector data

### Vector layers

The typical data structure for vector data is a vector layer.

Importing from file:


```python
path = gpd.datasets.get_path('naturalearth_lowres')
dat = gpd.read_file(path)
```

The result is a `GeoDataFrame`:


```python
dat
```

```
##        pop_est  ...                                           geometry
## 0       920938  ...  MULTIPOLYGON (((180.00000 -16.06713, 180.00000...
## 1     53950935  ...  POLYGON ((33.90371 -0.95000, 34.07262 -1.05982...
## 2       603253  ...  POLYGON ((-8.66559 27.65643, -8.66512 27.58948...
## 3     35623680  ...  MULTIPOLYGON (((-122.84000 49.00000, -122.9742...
## 4    326625791  ...  MULTIPOLYGON (((-122.84000 49.00000, -120.0000...
## ..         ...  ...                                                ...
## 172    7111024  ...  POLYGON ((18.82982 45.90887, 18.82984 45.90888...
## 173     642550  ...  POLYGON ((20.07070 42.58863, 19.80161 42.50009...
## 174    1895250  ...  POLYGON ((20.59025 41.85541, 20.52295 42.21787...
## 175    1218208  ...  POLYGON ((-61.68000 10.76000, -61.10500 10.890...
## 176   13026129  ...  POLYGON ((30.83385 3.50917, 29.95350 4.17370, ...
## 
## [177 rows x 6 columns]
```

Basic plotting using the `.plot` method:


```python
# dat.plot()
```

### Geometry columns

...

### Geometries

...

## Raster data

...

## Coordinate Reference Systems

...

## Units

...

## Exercises

...

