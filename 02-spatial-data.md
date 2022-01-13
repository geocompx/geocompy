# (PART) Foundations {-}

# Geographic data in R {#spatial-class}




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

