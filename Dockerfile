FROM continuumio/miniconda3
# See https://stackoverflow.com/questions/72021249/
RUN conda config --add channels conda-forge && conda update -y conda \
  && conda install -y geopandas
RUN wget https://github.com/geocompr/py/archive/refs/heads/main.zip
RUN conda install -c conda-forge unzip 
