# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: OSMNX
#     language: python
#     name: osmnx
# ---

# # Introduction
#
# This is site contains ideas, code and an outline of a yet-to-be written book on *Geocomputation with Python*.
#
# ## Motivations
#
# This book, tentatively called Geocomputation with Python ('geocompy'), is motivated by the need for an introductory yet rigorous and up-to-date resource on working with geographic data in Python that demonstrates basic data structures and describes code for handling vector *and* raster datasets in an integrated way.
# There are many resources on Python packages for geographic research and various applications but, to the best of our knowledge, no other resource brings together the following features into a single home:
#
# 1. Small introductory textbook focuses on doing basic operations well
# 2. Integration of vector and raster datasets in the same book, and within each section
# 3. Clear explanation of the code and exercises to maximize learning for newcomers
# 4. Provision of lucid example datasets and meaningful operations to illustrate the applied nature of geographic research
#
# The book aims to supplement other resources in the ecosystem, as highlighted by comparison with the book's scope with existing and in-progress works:
#
# - [Learning Geospatial Analysis with Python](https://www.packtpub.com/product/learning-geospatial-analysis-with-python/9781783281138) and [Geoprocessing with Python](https://www.manning.com/books/geoprocessing-with-python) focuses on processing spatial data using low-level Python interfaces for GDAL, such as the `gdal`, `gdalnumeric`, and `ogr` [packages](https://gdal.org/api/python.html) from `osgeo`. 
# This approach is more complex, [less "Pythonic"](https://rasterio.readthedocs.io/en/latest/intro.html#philosophy), and perhaps outdated in light of development of packages such as `geopandas` and `rasterio` covered here
# - [pythongis.org](https://pythongis.org/) (at an early stage of development) seeks to provide a general introduction to 'GIS in Python', with parts focusing on Python essentials, using Python with GIS, and case studies. 
# Compared with pythongis.org, geocompy has a relatively narrow scope (1) and a greater focus on raster-vector interoperability
# - [geographicdata.science](https://geographicdata.science/book/intro.html) is an ambitious project with chapters dedicated to advanced topics, with Chapter 4 on [Spatial Weights](https://geographicdata.science/book/notebooks/04_spatial_weights.html) getting into complex topics relatively early, for example.
# Geocompy would be shorter, simpler and more introductory, and cover raster and vector data with equal importance (1 to 4)
#
# Geocompy is a sister project of [Geocomputation with R](https://geocompr.robinlovelace.net/) -- a book on geographic data analysis, visualization, and modeling using the R programming language.
#
# ## Reproducing this book
# <!-- Would this live better in the README? (RL 2022-02-16) -->
#
# An important aspect of scientific research and 'citizen science' that is participatory is reproducibility of results.
# We aim to make this web version of the book as easy as possible. See the source code for details (work in progress).
#
# ### Reproduce the book locally
#
# First, download the book sample data into your working directory, and place them in a sub-directory named `"data"` inside that working directory.
#
# For Windows, follow these steps:
#
# * Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) either by:
#   - Downloading and running the .exe link manually, or
#   - With the [command](https://community.chocolatey.org/packages/miniconda3) `choco install miniconda3` from a PowerShell terminal after installing [Chocolatey](https://chocolatey.org/install)
# * Open the Anaconda Prompt (or a fresh PowerShell terminal after running the command [`conda init powershell`](https://github.com/conda/conda/issues/8428#issuecomment-474867193) from the Anaconda prompt), navigate to the above-mentioned working directory, and then run:
#
# ```sh
# conda env create -f environment.yml
# ```
#
# Activate the new environment with
#
# ```sh
# conda activate geocompy # the default name of the environment
# ```
#
# Reproduce a live preview of the book with the following command, which reqires that you have installed [quarto](https://quarto.org/):
#
# ```sh
# quarto preview # generate live preview of the book
# ```
#
# * Open the Jupyter Notebook of any of chapters using a command such as:
#
# ```sh
# jupyter notebook 02-spatial-data.ipynb
# ```
#
# The above steps should also work on Linux and Mac operating systems.
# Install conda, e.g. with the following commands in a Linux terminal:
#
# ```bash
# bash wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh
# ```
# You should see prompts like this:
#
# ```
# Please answer 'yes' or 'no':'
# >>> yes
#
# Miniconda3 will now be installed into this location:
# /home/robin/miniconda3
#
#   - Press ENTER to confirm the location
#   - Press CTRL-C to abort the installation
#   - Or specify a different location below
# ```
#
# After that you should be able to run the `conda create env` command above from bash to install the dependencies.
#
# For Linux, use your preferred package manager to install the packages used in the book (`geopandas`, `rasterio`, etc.) as specified in each chapter, as well as the Jupyter Notebook interface. For example, using `pip` to install the Jupyter Notebook package is as follows:
#
# ```sh
# pip install jupyter-book
# ```
#
# Then, navigate to the above-mentioned working directory, and open the Jupyter Notebook of any of chapters using a command such as:
#
# ```sh
# jupyter notebook 02-spatial-data.ipynb
# ```
#
# You can also install individual packages with:
#
# ```sh
# conda install jupyter # for example
# ```
#
# ### Reproduce the book in a Docker container with VSCode IDE
#
# Todo: help wanted
#
# ### Reproduce the book in a Docker container with IPython notebook
#
# Todo: help wanted
#
# ### Reproduce the book in a Docker container with RStudio IDE
#
# ```bash
# docker pull geocompr/geocompr:python
# # Remove the --rm below for a persistent image
# docker run --rm -d -p 8784:8787 -e DISABLE_AUTH=TRUE --name geocompy \
#   -v $(pwd):/home/rstudio/pytest geocompr/geocompr:python
# firefox localhost:8784 # or your browser of choice
# # docker kill geocompy # stop the image
# ```
#
# After opening the relevant project running `quarto preview` in the system shell in browser-based IDE opened by the command above, you should see something like this where you can run code and even modify the book and see changes with the previou command.
#
# ![](https://user-images.githubusercontent.com/1825120/156414301-bfe622c5-1290-4f85-8a21-08d2a6d77df1.png)
#
# ### Reproduce the book in Binder
#
# Todo: help wanted
#
# ```{bash, eval=FALSE, echo=FALSE}
# # Todo: improve these instructions before showing these system commands
# # To reproduce the book you need Python and and geo packages installed
# # Install them through a framework such as Conda (recommended) or pip3 as follows:
# pip3 install geopandas rasterio rioxarray jupyter matplotlib netcdf4 h5netcdf 
# # install quarto...
# quarto preview
#
# # Run the book code on Docker:
# ```
#
