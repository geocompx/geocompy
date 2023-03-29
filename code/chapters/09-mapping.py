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

# # Making maps with Python {#map-making}
#
# ## Introduction
#
# - Geopandas explore has been used in previous chapters.
# - When to focus on visualisation? At the end of geographic data processing workflows.
#
# <!-- Input datasets: https://github.com/geocompr/spDatapy -->
# <!-- Decision of whether to use static or interactive. -->
# <!-- Flow diagram? -->

#| echo: false
#| label: getdata
from pathlib import Path
data_path = Path("data")
if data_path.is_dir():
  pass
  # print("path exists") # directory exists
else:
  print("Attempting to get and unzip the data")
  import requests, zipfile, io
  r = requests.get("https://github.com/geocompx/geocompy/releases/download/0.1/data.zip")
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall(".")

import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import rasterio.plot
nz = gpd.read_file("data/nz.gpkg")

# ## Static maps
#
# - Focus on matlibplot
# - First example: NZ with fill and borders
# - Scary matplotlib code here...

#| layout-ncol: 3
nz.plot(color="grey");
nz.plot(color="none", edgecolor="blue");
nz.plot(color="grey", edgecolor="blue");

# <!-- # Add fill layer to nz shape
# tm_shape(nz) +
#   tm_fill()
# # Add border layer to nz shape
# tm_shape(nz) +
#   tm_borders()
# # Add fill and border layers to nz shape
# tm_shape(nz) +
#   tm_fill() +
#   tm_borders()  -->
#
# As covered in Chapter 2, you can plot raster datasets as follows:

nz_elev = rasterio.open('data/nz_elev.tif')
rasterio.plot.show(nz_elev);

# <!--
# In R:
# nz_elev = stars::read_stars("data/nz_elev.tif")
# sf::st_crs(nz_elev)
# nz = spData::nz
# waldo::compare(sf::st_crs(nz), sf::st_crs(nz_elev))
# library(sf)
# plot(nz)
# nz_elev_transformed = sf::st_transform(nz_elev, sf::st_crs(nz))
# stars::write_stars(nz_elev_transformed, "data/nz_elev.tif")
# nz_transformed = sf::st_transform(nz, sf::st_crs(nz_elev))
# sf::st_write(nz_transformed, "nz_transformed.gpkg")
# -->
#
#
# You can combine the raster and vector plotting methods shown above into a single visualisation with multiple layers as follows:
#
# <!-- 
# Source:
# https://gis.stackexchange.com/questions/294072/how-can-i-superimpose-a-geopandas-dataframe-on-a-raster-plot
# -->

fig, ax = plt.subplots(figsize=(5, 5))
rasterio.plot.show(nz_elev, ax=ax)
nz.to_crs(nz_elev.crs).plot(ax=ax, facecolor='none', edgecolor='r');

# ### Palettes
# ### Layers
# ### Faceted maps
# ### Exporting maps as images
#
# <!-- ## Animated maps -->
#
# ## Interactive maps
#
# - When are interactive maps useful
#
# An interactive map is an important way to understand and interpret complex geographical information. A good interactive map enables movement across the map area, change the area of interest and provide additional context or text information. In this section we will look an interactive map based of national public transport access nodes (NaPTAN), the UK Department for Transport repository of public transport point-of-interest in England, Scotland and Wales consisting of:
# - bus stops and railway stations
# - tram, metro and underground stops
# - airports and ferry terminals
#
#
# We will show how to create this may restricted to railway stations, tram stops and ferry terminals in Yorkshire. This will also match data to the National Rail customer reservation code (CRS) and timing point location (TIPLOC) attributes used in the the national rail timetable.
#
# In the first code block we define a function `get_databuffer` that uses the `requests` library to download the NaPTAN data-set in CSV format to a `StringIO` buffer.

# +
#| eval: false
import io
import requests

def get_databuffer(uri, encoding='UTF-8'):
    """Download data from URI and returns as an StringIO buffer"""
    r = requests.get(uri, timeout=10)
    return io.StringIO(str(r.content, encoding))

# NaPTAN data service
URI='https://multiple-la-generator-dot-dft-add-naptan-prod.ew.r.appspot.com/v1/access-nodes?dataFormat=csv'
BUFFER = get_databuffer(URI)
# -

# We then read the in-memory string-buffer into a `Panda` data-frame, treating the buffer as if it were a CSV file. We then extract the location data into a `numpy` two-dimensional array.

# +
#| eval: false
import pandas as pd

DF1 = pd.read_csv(BUFFER, low_memory=False)
DATA = DF1[['Longitude', 'Latitude']].values
# -

# We then convert the $transposed data-array$ into a `GeoSeries` and use this to create a `GeoDataFrame`. Which we then tidy by dropping any columns that only contain invalid (`pd.NA`) values.

# +
#| eval: false
import geopandas as gpd

POINTS = gpd.points_from_xy(*DATA.T, crs='WGS84')
NaPTAN = gpd.GeoDataFrame(data=DF1, geometry=POINTS)

NaPTAN = NaPTAN.dropna(how='all', axis=1)
# -

# The next step is to create the timing-point `TIPLOC` data based on the `StopType` and a subset of the `ATCOCode` columns.

# +
#| eval: false
NaPTAN['TIPLOC'] = ''
# Heavy railway stations
IDX1 = NaPTAN['StopType'] == 'RLY'
NaPTAN.loc[IDX1, 'TIPLOC'] = NaPTAN['ATCOCode'].str[4:]

# Ferrys
IDX1 = NaPTAN['StopType'] == 'FER'
NaPTAN.loc[IDX1, 'TIPLOC'] = NaPTAN['ATCOCode'].str[4:]

# Metro and trams
IDX1 = NaPTAN['StopType'] == 'MET'
NaPTAN.loc[IDX1, 'TIPLOC'] = NaPTAN['ATCOCode'].str[6:]
# -

# We extract the heavy and light rail, or ferry locationsFrom the 435,298 rows in the NaPTAN data-frame.

#| eval: false
IDX1 = NaPTAN['StopType'].isin(['RLY', 'FER', 'MET'])
STATIONS = NaPTAN[IDX1]

# Filter columns and drop points within Yorkshire.

# +
#| eval: false
FIELDS = ['ATCOCode', 'CommonName', 'ShortCommonName', 'LocalityName',
          'StopType', 'Status', 'TIPLOC', 'geometry']

# Clean up data-frame columns
STATIONS = STATIONS[FIELDS]

YORKSHIRE = gpd.read_file('data/yorkshire.json').iloc[0, 0]
IDX = STATIONS.within(YORKSHIRE)

STATIONS = STATIONS[IDX]

# Write to GeoJSON
STATIONS.to_file('stations.geojson', driver='GeoJSON')
# Write file to GeoPackage

OUTPUT = STATIONS.copy()
CRS = 'EPSG:32630'
OUTPUT['geometry'] = OUTPUT['geometry'].to_crs(CRS)
OUTPUT.to_file('stations.gpkg', driver='GPKG', layer='stations')
# -

# - Holoviews: facetted plotting
# - Panel: allows you to create applications/dashboards
#
# ### GeoPandas explore
# ### Layers
# ### Publishing interactive maps
# ### Linking geographic and non-geographic visualisations
#
# <!-- ## Mapping applications Streamlit? -->
#
# ## Exercises
