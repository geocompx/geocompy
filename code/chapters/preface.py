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

# ## Preface {.unnumbered}
#
# **Geocomputation with Python** (*geocompy*) is motivated by the need for an introductory, yet rigorous and up-to-date, resource geographic data with the most popular programming language in the world.
# A unique selling point of the book is its cohesive and joined-up coverage of *both vector and raster* geographic data models and consistent learning curve.
# We aim to *minimize surprises*, with each section and chapter building on the previous.
# If you're just starting out with Python for working with geographic data, this book is an excellent place to start.
#
# There are many resources on Python on 'GeoPython' but none that fill this need for an introductory resource that provides strong foundations for future work.
# We want to avoid reinventing the wheel and provide something that fills an 'ecological niche' in the wider free and open source software for geospatial (FOSS4G) ecosystem.
# Key features include:
#
# 1. Doing basic operations well
# 2. Integration of vector and raster datasets and operations
# 3. Clear explanation of each line of code in the book to minimize surprises
# 4. Excercises at the end of each chapter with reproducible and open solutions
# 5. Provision of lucid example datasets and meaningful operations to illustrate the applied nature of geographic research
#
# This book is complementary with, and adds value to, other projects in the ecosystem, as highlighted in the following comparison between *Geocomputation with Python* and related GeoPython books:
#
# - [Learning Geospatial Analysis with Python](https://www.packtpub.com/product/learning-geospatial-analysis-with-python/9781783281138) and [Geoprocessing with Python](https://www.manning.com/books/geoprocessing-with-python) are books in this space that focus on processing spatial data using low-level Python interfaces for GDAL, such as the **gdal**, **gdalnumeric**, and **ogr** [packages](https://gdal.org/api/python_bindings.html) from **osgeo**. 
# This approach requires writing more lines of code. 
# We believe our approach is more ["Pythonic"](https://rasterio.readthedocs.io/en/latest/intro.html#philosophy) and future-proof, in light of development of packages such as **geopandas** and **rasterio**.
# - [Introduction to Python for Geographic Data Analysis](https://pythongis.org/) (in progress) seeks to provide a general introduction to 'GIS in Python', with parts focusing on Python essentials, using Python with GIS, and case studies. 
# Compared with this book, which is also open source, and is hosted at pythongis.org, *Geocomputation with Python* has a narrower scope (not covering [spatial network analysis](https://pythongis.org/part3/chapter-11/index.html), for example) and more coverage of raster data processing and raster-vector interoperability.
# - [Geographic Data Science with Python](https://geographicdata.science/book/intro.html) is an ambitious project with chapters dedicated to advanced topics, with Chapter 4 on [Spatial Weights](https://geographicdata.science/book/notebooks/04_spatial_weights.html) getting into complex topics relatively early, for example.
# Geocompy is shorter, simpler and more introductory, and cover raster and vector data with equal importance (1 to 4).
#
# Another unique feature of the book is that it is part of a wider community.
# *Geocomputation with Python* is a sister project of [Geocomputation with R](https://r.geocompx.org/), a book on geographic data analysis, visualization, and modeling using the R programming language that has 60+ contributors and an active community, not least in the associated [Discord group](https://discord.gg/PMztXYgNxp).
# Links with the vibrant 'R-spatial' community, and other communities such as [GeoRust](https://georust.org/) and [JuliaGeo](https://juliageo.org/), will lead to many opportunities for mutual benefit across open source ecosystems.
