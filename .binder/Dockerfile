FROM geocompr/geocompr:binder

# Install Python: https://github.com/geocompr/docker/blob/master/geocompy/Dockerfile
RUN wget https://github.com/rocker-org/rocker-versioned2/raw/master/scripts/install_python.sh
RUN bash install_python.sh
# Install Python packages for vector data:
RUN pip3 install geopandas movingpandas pykdtree scipy topojson
# Install Python packages for raster data:
RUN pip3 install rasterio rioxarray netcdf4 h5netcdf
# Install Python packages for visualisation
RUN pip3 install jupyter matplotlib hvplot geoviews # pyviz # seems to fail
# Install quarto
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/etc/apt/trusted.gpg.d/githubcli-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
RUN apt update
RUN apt install gh
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v0.9.56/quarto-0.9.56-linux-amd64.deb
RUN dpkg -i quarto*
RUN quarto --version
## Declares build arguments
ARG NB_USER
ARG NB_UID

COPY --chown=${NB_USER} . ${HOME}

ENV DEBIAN_FRONTEND=noninteractive
USER root
RUN echo "Checking for 'apt.txt'..." \
        ; if test -f "apt.txt" ; then \
        apt-get update --fix-missing > /dev/null\
        && xargs -a apt.txt apt-get install --yes \
        && apt-get clean > /dev/null \
        && rm -rf /var/lib/apt/lists/* \
        ; fi
USER ${NB_USER}
