FROM continuumio/miniconda3

# See https://pythonspeed.com/articles/conda-docker-image-size/
# RUN environment.yml .
RUN wget https://github.com/geocompr/py/raw/main/environment.yml

RUN conda env create -f environment.yml

# ENTRYPOINT ["conda", "run", "-n", "geocompy", \
#             "python", "-c", \
#             "import numpy; print('success!')"]
# See https://stackoverflow.com/questions/72021249/
# RUN conda config --add channels conda-forge && conda update -y conda \
#   && conda install -y geopandas
# RUN wget https://github.com/geocompr/py/archive/refs/heads/main.zip
# RUN conda install -c conda-forge unzip 
