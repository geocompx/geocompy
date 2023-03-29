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

# # Attribute data operations {#attr}
#
# ## Prerequisites

#| echo: false
import pandas as pd
import matplotlib.pyplot as plt
pd.options.display.max_rows = 6
pd.options.display.max_columns = 6
pd.options.display.max_colwidth = 35
plt.rcParams['figure.figsize'] = (5, 5)

# Packages...

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio

# Sample data...

# +
#| echo: false
import os
from urllib.request import urlretrieve

data_path = 'data'
if not os.path.exists(data_path):
  os.mkdir(data_path)
  
file_path = 'data/landsat.tif'
url = 'https://github.com/geocompx/geocompy/releases/download/0.1/landsat.tif'
if not os.path.exists(file_path):
  print('Attempting to get the data')
  urlretrieve(url, file_path)
# -

world = gpd.read_file('data/world.gpkg')
src_elev = rasterio.open('data/elev.tif')
src_multi_rast = rasterio.open('data/landsat.tif')

# ## Introduction
#
# Attribute data is non-spatial information associated with geographic (geometry) data.
# A bus stop provides a simple example: its position would typically be represented by latitude and longitude coordinates (geometry data), in addition to its name.
# The Elephant & Castle / New Kent Road stop in London, for example has coordinates of `-0.098` degrees longitude and `51.495` degrees latitude which can be represented as `POINT (-0.098 51.495)` in the Simple Feature representation described in @sec-spatial-class.
# Attributes such as the name attribute of the `POINT` feature (to use Simple Features terminology) are the topic of this chapter.
#
# Another example is the elevation value (attribute) for a specific grid cell in raster data. Unlike the vector data model, the raster data model stores the coordinate of the grid cell indirectly, meaning the distinction between attribute and spatial information is less clear.
# To illustrate the point, think of a pixel in the 3rd row and the 4th column of a raster matrix.
# Its spatial location is defined by its index in the matrix: move from the origin four cells in the x direction (typically east and right on maps) and three cells in the y direction (typically south and down).
# The raster's resolution defines the distance for each x- and y-step which is specified in a header.
# The header is a vital component of raster datasets which specifies how pixels relate to geographic coordinates (see also Chapter @spatial-operations).
#
# This chapter teaches how to manipulate geographic objects based on attributes such as the names of bus stops in a vector dataset and elevations of pixels in a raster dataset. 
# For vector data, this means techniques such as subsetting and aggregation (see @sec-vector-attribute-subsetting and @sec-vector-attribute-aggregation).
# @sec-vector-attribute-joining and @sec-creating-attributes-and-removing-spatial-information demonstrate how to join data onto simple feature objects using a shared ID and how to create new variables, respectively. 
# Each of these operations has a spatial equivalent: `[` operator for subsetting a `(Geo)DataFrame` using a boolean `Series`, for example, is applicable both for subsetting objects based on their attribute and spatial relations derived using methods such as `.intersects`; you can also join attributes in two geographic datasets using spatial joins. This is good news: skills developed in this chapter are cross-transferable.
# @sec-spatial-operations extends the methods presented here to the spatial world.
#
# After a deep dive into various types of vector attribute operations in the next section, raster attribute data operations are covered in @sec-manipulating-raster-objects, which demonstrates how to create raster layers containing continuous and categorical attributes and extracting cell values from one or more layer (raster subsetting). 
# @sec-summarizing-raster-objects provides an overview of 'global' raster operations which can be used to summarize entire raster datasets.
#
# ## Vector attribute manipulation
#
# As mentioned in @sec-vector-layers, vector layers (`GeoDataFrame`, from package **geopandas**) are basically extended tables (`DataFrame` from package **pandas**), the difference being that a vector layer has a geometry column.
# Since `GeoDataFrame` extends `DataFrame`, all ordinary table-related operations from package **pandas** are supported for vector layers as well, as shown below.
#
# ### Vector attribute subsetting {#sec-vector-attribute-subsetting}
#
# **pandas** supports several subsetting interfaces, though the most [recommended](https://stackoverflow.com/questions/38886080/python-pandas-series-why-use-loc) ones are:
#
# * `.loc`, which uses pandas indices, and
# * `.iloc`, which uses (implicit) numpy-style numeric indices.
#
# In both cases the method is followed by square brackets, and two indices, separated by a comma. Each index can comprise:
#
# * A specific value, as in `1`
# * A slice, as in `0:3`
# * A `list`, as in `[0,2,4]`
# * `:`—indicating "all" indices
#
# An exception to this rule is selecting columns using a list, as in `df[['a','b']]`, instead of `df.loc[:, ['a','b']]`, to select columns `'a'` and `'b'` from `df`.
#
# Here are few examples of subsetting the `GeoDataFrame` of world countries.
#
# Subsetting rows by position, e.g., the first three rows:

world.iloc[0:3, :]

# which is equivalent to:

world.iloc[:3]

# as well as:

world.head(3)

# Subsetting columns by position, e.g., the first three columns:

world.iloc[:, 0:3]

# Subsetting rows and columns by position:

world.iloc[0:3, 0:3]

# Subsetting columns by name:

world[['name_long', 'geometry']]

# "Slice" of columns between given ones:

world.loc[:, 'name_long':'pop']

# Subsetting by a list of boolean values (0 and 1 or True and False):

x = [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0] 
world.iloc[:, x]

# We can remove specific rows by id using the `.drop` method, e.g., dropping rows 2, 3, and 5:

world.drop([2, 3, 5])

# Or remove specific columns using the `.drop` method and `axis=1` (i.e., columns):

world.drop(['name_long', 'continent'], axis=1)

# We can rename columns using the `.rename` method:

world[['name_long', 'pop']].rename(columns={'pop': 'population'})

# The standard **numpy** comparison operators can be used in boolean subsetting, as illustrated in Table @tbl-comparison-operators.
#
# |`Symbol` | `Name` | 
# |---|---|
# | `==` | Equal to |
# | `!=` | Not equal to |
# | `>`, `<` | Greater/Less than |
# | `>=`, `<=` | Greater/Less than or equal |
# | `&`, `|`, `~` | Logical operators: And, Or, Not |
#
# : Comparison operators that return Booleans (`True`/`False`). {#tbl-comparison-operators}
#
# The following example demonstrates logical vectors for subsetting by creating a new `GeoDataFrame` object called `small_countries` that contains only those countries whose surface area is smaller than 10,000 km^2^:

idx_small = world['area_km2'] < 10000  ## a logical 'Series'
small_countries = world[idx_small]
small_countries

# The intermediary `idx_small` (short for index representing small countries) is a boolean `Series` that can be used to subset the seven smallest countries in the world by surface area.
# A more concise command, which omits the intermediary object, generates the same result:

small_countries = world[world['area_km2'] < 10000]
small_countries

# The various methods shown above can be chained for any combination with several subsetting steps, e.g.:

world[world['continent'] == 'Asia']  \
    .loc[:, ['name_long', 'continent']]  \
    .iloc[0:5, :]

# We can also combine indexes:

idx_small = world['area_km2'] < 10000
idx_asia = world['continent'] == 'Asia'
world.loc[idx_small & idx_asia, ['name_long', 'continent', 'area_km2']]

# ### Vector attribute aggregation {#sec-vector-attribute-aggregation}
#
# Aggregation involves summarizing data based on one or more *grouping variables* (typically values in a column;geographic aggregation is covered in the next chapter). A classic example of this attribute-based aggregation is calculating the number of people per continent based on country-level data (one row per country).
# The `world` dataset contains the necessary ingredients: the columns `pop` and `continent`, the population and the grouping variable, respectively. The aim is to find the `sum()` of country populations for each continent, resulting in a smaller data frame. (Since aggregation is a form of data reduction, it can be a useful early step when working with large datasets). This aggregation can be achieved using a combination of `.groupby` and `.sum`:

world_agg1 = world[['continent', 'pop']].groupby('continent').sum()
world_agg1

# If you dislike the scientific notation used by default to display the population sums, you can change the Pandas display format for float values like this: 

pd.set_option('display.float_format', '{:.0f}'.format)
world_agg1

# The result is a (non-spatial) table with eight rows, one per continent, and two columns reporting the name and population of each continent.
#
# If we want to include the geometry in the aggregation result, we can use the `.dissolve` method.
# That way, in addition to the summed population, we also get the associated geometry per continent, i.e., the union of all countries.
# Note that we use the `by` parameter to choose which column(s) are used for grouping, and the `aggfunc` parameter to choose the aggregation function for non-geometry columns:

world_agg2 = world[['continent', 'pop', 'geometry']] \
    .dissolve(by='continent', aggfunc='sum') \
    .reset_index()
world_agg2

# @fig-spatial-aggregation shows the result:

# +
#| label: fig-spatial-aggregation
#| fig-cap: Continents with summed population

world_agg2.plot(column='pop', legend=True);
# -

# The resulting `world_agg2` object is a `GeoDataFrame` containing 8 features representing the continents of the world (and the open ocean). 
#
# Other options for the `aggfunc` parameter in `.dissolve` [include](https://geopandas.org/en/stable/docs/user_guide/aggregation_with_dissolve.html):
#
# * `'first'`
# * `'last'`
# * `'min'`
# * `'max'`
# * `'sum'`
# * `'mean'`
# * `'median'`
#
# Additionally, we can pass custom functions.
#
# As a more complex example, here is how we can calculate the total population, area, and count of countries, per continent:

world_agg3 = world.dissolve(
    by='continent', aggfunc={
         "name_long": "count",
         "pop": "sum",
         'area_km2': "sum"
     }).rename(columns={'name_long': 'n'})
world_agg3

# Figure @fig-spatial-aggregation-different-functions visualizes the resulting layer (`world_agg3`) of continents with the three aggregated attributes.

# +
#| label: fig-spatial-aggregation-different-functions
#| fig-cap: 'Continent properties, calculated using spatial aggregation using different functions'

fig, axes = plt.subplots(2, 2, figsize=(9, 5))
world_agg3.plot(column='pop', edgecolor='black', legend=True, ax=axes[0][0])
world_agg3.plot(column='area_km2', edgecolor='black', legend=True, ax=axes[0][1])
world_agg3.plot(column='n', edgecolor='black', legend=True, ax=axes[1][0])
axes[0][0].set_title('Summed population')
axes[0][1].set_title('Summed area')
axes[1][0].set_title('Count of countries')
fig.delaxes(axes[1][1]);
# -

# Let's proceed with the last result to demonstrate other table-related operations. Given the `world_agg3` continent summary (@fig-spatial-aggregation-different-functions), we:
#
# * drop the geometry columns, 
# * calculate population density of each continent, 
# * arrange continents by the number countries they contain, and 
# * keep only the 3 most populous continents. 

world_agg4 = world_agg3.drop(columns=['geometry'])
world_agg4['density'] = world_agg4['pop'] / world_agg4['area_km2']
world_agg4 = world_agg4.sort_values(by='n', ascending=False)
world_agg4 = world_agg4.head(3)
world_agg4

# ### Vector attribute joining {#sec-vector-attribute-joining}
#
# Combining data from different sources is a common task in data preparation. Joins do this by combining tables based on a shared 'key' variable. 
# **pandas** has a function named `pd.merge` for joining `(Geo)DataFrames` based on common column(s).
# The `pd.merge` function follows conventions used in the database language SQL (Grolemund and Wickham 2016). 
# The `pd.merge` function works the same on `DataFrame` and `GeoDataFrame` objects.
# The result of `pd.merge` can be either a `DataFrame` or a `GeoDataFrame` object, depending on the inputs.
#
# A common type of attribute join on spatial data is to join `DataFrames` to `GeoDataFrames`.
# To achieve this, we use `pd.merge` with a `GeoDataFrame` as the first argument and add columns to it from a `DataFrame` specified as the second argument.
# In the following example, we combine data on coffee production with the `world` dataset.
# The coffee data is in a `DataFrame` called `coffee_data` imported from a CSV file of major coffee-producing nations:

coffee_data = pd.read_csv('data/coffee_data.csv')
coffee_data

# Its three columns are: 
#
# * `name_long` country name 
# * `coffee_production_2016` and `coffee_production_2017` contain estimated values for coffee production in units of 60-kg bags per year.
#
# A left join, which preserves the first dataset, merges `world` with `coffee_data`, based on the common `'name_long'` column:

world_coffee = pd.merge(world, coffee_data, on='name_long', how='left')
world_coffee

# The result is a `GeoDataFrame` object identical to the original `world` object, but with two new variables (`coffee_production_2016` and `coffee_production_2017`) on coffee production.
# This can be plotted as a map, as illustrated in @fig-join-coffee-production:

# +
#| label: fig-join-coffee-production
#| fig-cap: 'World coffee production, thousand 60-kg bags by country, in 2017 (source: International Coffee Organization).'

base = world_coffee.plot(color='white', edgecolor='lightgrey')
coffee_map = world_coffee.plot(ax=base, column='coffee_production_2017')
coffee_map.set_title('Coffee production');
# -

# To work, attribute-based joins need a 'key variable' in both datasets (`on` parameter of `pd.merge`). 
# In the above example, both `world_coffee` and `world` DataFrames contained a column called `name_long`.
# (By default `pd.merge` uses all columns with matching names. However, it is recommended to explicitly specify the names of the columns to be used for matching, like we did in the last example.)
#
# In case where column names are not the same, you can use `left_on` and `right_on` to specify the respective columns.
#
# Note that the result `world_coffee` has the same number of rows as the original dataset `world`.
# Although there are only 47 rows in `coffee_data`, all 177 country records are kept intact in `world_coffee`. Rows in the original dataset with no match are assigned `np.nan` values for the new coffee production variables. 
# This is a characteristic of a left join (specified with `how='left'`) and is what we typically want to do. 
#
# What if we only want to keep countries that have a match in the key variable?
# In that case an inner join can be used:

pd.merge(world, coffee_data, on='name_long', how='inner')

# An alternative way to join two (Geo)DataFrames is the aptly called `join` function: 

world.join(coffee_data.set_index('name_long'), on='name_long', how='inner')

# Note that in this case, we need to set the index of `coffee_data` to the `name_long` values to avoid error messages.
#
# ### Creating attributes and removing spatial information {#sec-creating-attributes-and-removing-spatial-information}
#
# Often, we would like to create a new column based on already existing columns. For example, we want to calculate population density for each country. For this we need to divide a population column, here `pop`, by an area column, here `area_km2`. Note that we are working on a copy of `world` named `world2` so that we do not modify the original layer:

world2 = world.copy()
world2['pop_dens'] = world2['pop'] / world2['area_km2']
world2

# To paste (i.e., concatenate) together existing columns, we can use the ordinary Python string operator `+`, as if we are working with individual strings rather than `Series`. For example, we want to combine the `continent` and `region_un` columns into a new column named `con_reg`, using `':'` as a separator. Subsequesntly, we remove the original columns using `.drop`:

world2['con_reg'] = world['continent'] + ':' + world2['region_un']
world2 = world2.drop(['continent', 'region_un'], axis=1)
world2

# The resulting sf object has a new column called `con_reg` representing the continent and region of each country, e.g., `'South America:Americas'` for Argentina and other South America countries. The opposite operation, splitting one column into multiple columns based on a separator string, is done using the `.str.split` method. As a result we go back to the previous state of two separate `continent` and `region_un` columns (only that their position is now last, since they are newly created):

world2[['continent', 'region_un']] = world2['con_reg'] \
    .str.split(':', expand=True)
world2

# Renaming one or more columns can be done using the `.rename` method combined with the `columns` argument, which should be a dictionary of the form `old_name:new_name`. The following command, for example, renames the lengthy `name_long` column to simply `name`:

world2.rename(columns={'name_long': 'name'})

# To change all column names at once, we assign a `list` of the "new" column names into the `.columns` property. The `list` must be of the same length as the number of columns (i.e., `world.shape[1]`). This is illustrated below, which outputs the same `world2` object, but with very short names:

new_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'geom', 'i', 'j', 'k', 'l']
world2.columns = new_names
world2

# To reorder columns, we can pass a modified columns list to the subsetting operator `[`. For example, the following expressions reorder `world2` columns in reverse alphabetical order:

names = sorted(world2.columns, reverse=True)
world2 = world2[names]
world2

# Each of these attribute data operations, even though they are defined in the `pandas` package and applicable to any `DataFrame`, preserve the geometry column and the `GeoDataFrame` class. Sometimes, however, it makes sense to remove the geometry, for example to speed-up aggregation or to export just the attribute data for statistical analysis. To go from `GeoDataFrame` to `DataFrame` we need to:
#
# 1. Drop the geometry column
# 1. Convert from `GeoDataFrame` into a `DataFrame`
#
# For example:

world2 = world2.drop('geom', axis=1)
world2 = pd.DataFrame(world2)
world2

# ## Manipulating raster objects {#sec-manipulating-raster-objects}
#
# ### Raster subsetting {#sec-raster-subsetting}
#
# When using `rasterio`, raster values are accessible through a `numpy` array, which can be imported with the `.read` method:

elev = src_elev.read(1)
elev

# Then, we can access any subset of cell values using `numpy` methods, e.g.:

elev[0, 0]  ## Value at row 1, column 1

# Cell values can be modified by overwriting existing values in conjunction with a subsetting operation, e.g. to set the upper left cell of elev to 0:

elev[0, 0] = 0
elev

# Multiple cells can also be modified in this way:

elev[0, 0:3] = 0
elev

# ### Summarizing raster objects {#sec-summarizing-raster-objects}
#
# Global summaries of raster values can be calculated by applying `numpy` summary functions on the array with raster values, e.g. `np.mean`:

np.mean(elev)

# Note that "No Data"-safe functions--such as `np.nanmean`---should be used in case the raster contains "No Data" values which need to be ignored. Before we can demontrate that, we must convert the array from `int` to `float`, as `int` arrays cannot contain `np.nan` (due to computer memory limitations):

elev1 = elev.copy()
elev1 = elev1.astype('float64')
elev1

# Now we can insert an `np.nan` value into the array. (Trying to do so in the original `elev` array raises an error, try it to see for yourself)

elev1[0, 2] = np.nan
elev1

# With the `np.nan` value inplace, the summary value becomes unknown:

np.mean(elev1)

# Therefore, we need to ignore the "No Data" value(s):

np.nanmean(elev1)

# Raster value statistics can be visualized in a variety of ways. 
# One approach is to "flatten" the raster values into a one-dimensional array, then use a graphical function such as `plt.hist` or `plt.boxplot` (from `matplotlib.pyplot`).
# For example:

x = elev.flatten()
plt.hist(x);

# ## Exercises
#
