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
  r = requests.get("https://github.com/geocompr/py/releases/download/0.1/data.zip")
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall(".")

import matplotlib as mpl
import geopandas as gpd
nz = gpd.read_file("data/nz.gpkg") 

# ## Static maps
#
# - Focus on matlibplot
# - First example: NZ with fill and borders
# - Scary matplotlib code here...

nz.plot(color="grey")
nz.plot(color="none", edgecolor="blue")

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
# ### Palettes
# ### Layers
# ### Faceted maps
# ### Exporting maps as images
#
# <!-- ## Animated maps -->
# ## Interactive maps
#
# - When are interactive maps useful
# - Holoviews: facetted plotting
# - Panel: allows you to create applications/dashboards
#
# ### GeoPandas explore
import io
import pandas as pd
import requests

pd.set_option('display.max_columns', None)

CRS = 'EPSG:32630'

def get_databuffer(uri, encoding='utf-8'):
    """Download data from URI and returns as an StringIO buffer"""
    r = requests.get(uri, timeout=10)
    return io.StringIO(str(r.content, encoding))

def download_data(uri, filepath='./NaPTAN.csv'):
    """Download data from URI and returns save to file system """
    with open(filepath, 'wb') as fout:
        data = requests.get(uri)
        fout.write(data.content)
    return True

# NaPTAN data service
URI='https://multiple-la-generator-dot-dft-add-naptan-prod.ew.r.appspot.com/v1/access-nodes?dataFormat=csv'

BUFFER = get_databuffer(URI)
DF1 = pd.read_csv(BUFFER, low_memory=False)
DATA = DF1[['Longitude', 'Latitude']].values
POINTS = gpd.GeoSeries.from_xy(*DATA.T, crs='WGS84')
NaPTAN = gpd.GeoDataFrame(data=DF1, geometry=POINTS)
NaPTAN = NaPTAN.to_crs(CRS).dropna(how='all', axis=1)

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

URI='https://www.nationalrail.co.uk/station_codes%20(07-12-2020).csv'
BUFFER = get_databuffer(URI)
DATA = pd.read_csv(BUFFER, low_memory=False)
DATA.columns = ['Station Name', 'CRS'] * 4
CRScode = pd.concat([DATA.iloc[:, 0:2], DATA.iloc[:, 2:4], DATA.iloc[:, 4:6], DATA.iloc[:, 6:]])
CRScode = CRScode.dropna().reset_index(drop=True)
CRScode = CRScode.set_index('Station Name')

# Ignore all locations other than heavy and light rail, or ferry locations
IDX1 = NaPTAN['StopType'].isin(['RLY', 'FER', 'MET'])

# Add CRS codes to train stations
STATIONS = NaPTAN[IDX1].join(CRScode, on='LocalityName')
STATIONS['Status'] = STATIONS['Status'].fillna(STATIONS['Modification'])
STATIONS = STATIONS.dropna(how='all', axis=1).reset_index().fillna('')

FIELDS = ['ATCOCode', 'CommonName', 'ShortCommonName', 'LocalityName',
          'StopType', 'Status', 'TIPLOC', 'CRS', 'geometry']

# Clean up data-frame columns
STATIONS = STATIONS[FIELDS]

# Write to GeoJSON
STATIONS.to_crs(CRS).to_file('stations.geojson', driver='GeoJSON')
# Write file to GeoPackage
STATIONS.to_crs(CRS).to_file('stations.gpkg', driver='GPKG', layer='stations')

# ### Layers
# ### Publishing interactive maps
# ### Linking geographic and non-geographic visualisations
#
# <!-- ## Mapping applications Streamlit? -->
#
# ## Exercises
