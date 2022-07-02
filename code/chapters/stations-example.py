import io
import numpy as np
import folium
import pandas as pd
import requests

pd.set_option('display.max_columns', None)

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

try:
  DF1
except NameError:
  BUFFER = get_databuffer(URI)
  DF1 = pd.read_csv(BUFFER, low_memory=False)
  DATA = DF1[['Longitude', 'Latitude']].values
  POINTS = gpd.GeoSeries.from_xy(*DATA.T, crs='WGS84')

def _set_precision(precision=0):
  """returns function that rounds a geometry to a given precision""" 
  from functools import partial
  from shapely.ops import transform

  def _precision(x, y, z=None):
    return tuple([round(i, precision) for i in [x, y, z] if i])
  return partial(transform, _precision)

_precision = _set_precision(3)
POINTS = POINTS.apply(_precision)
NaPTAN = gpd.GeoDataFrame(data=DF1, geometry=POINTS)

NaPTAN = NaPTAN.dropna(how='all', axis=1)
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

URI = 'https://www.nationalrail.co.uk/station_codes%20(07-12-2020).csv'
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

YORKSHIRE = gpd.read_file('data/yorkshire.json').iloc[0, 0]
IDX = STATIONS.within(YORKSHIRE)

STATIONS = STATIONS[IDX]

def get_colour(p):
  if p.StopType == 'MET':
    return "#41B6C4"
  if p.StopType == 'FER':
    return "#225EA8"
  if p.Status == 'active':
    return "#0C2C84"
  if p.Status == 'inactive':
    return "#FFFFCC"
  return "#ff00ff"

def get_popup(d):
  fields = ['ATCOCode', 'LocalityName', 'StopType', 'Status', 'TIPLOC', 'CRS']
  r = f'{d.CommonName}'
  for k, v in p[fields].to_dict().items():
    if v:
      r += f'<br>{k}: {v}'
  return folium.Popup(r, max_width=200)

MAP = folium.Map(location=[54.033, -2.03], zoom_start=8, width=1340, height=780)

for i, p in STATIONS.iterrows():
  try:
    folium.Circle(
      location=[p['geometry'].y, p['geometry'].x],
      popup=get_popup(p[FIELDS]),
      maxWidth=1000,
      radius=800,
      color=get_colour(p),
      fill=True,
      opacity=0.4,
      fill_color=get_colour(p),
      stroke=True,
      weight=1.0,
      linewidth=1.0,
    ).add_to(MAP)
  except IndexError:
    pass

MAP.save('index.html')

# Write to GeoJSON
STATIONS.to_file('stations.geojson', driver='GeoJSON')
# Write file to GeoPackage

OUTPUT = STATIONS.copy() 
CRS = 'EPSG:32630'
_precision = _set_precision(0)
OUTPUT['geometry'] = OUTPUT['geometry'].to_crs(CRS).apply(_precision)
OUTPUT.to_file('stations.gpkg', driver='GPKG', layer='stations')
