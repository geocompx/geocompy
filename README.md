# geocompy

[![Render](https://github.com/geocompr/py/actions/workflows/main.yaml/badge.svg)](https://github.com/geocompr/py/actions/workflows/main.yaml)
[![Binder](http://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/geocompr/py/main?urlpath=lab/tree/ipynb)

<https://geocompr.github.io/py/>

Broadly, the book can be reproduced after following three steps:

1. Install Quarto https://quarto.org/docs/get-started/
2. Install Jupyter, RStudio or VS Code
3. Install the Python dependencies with `miniconda3` (recommended) or Docker

Detailed instructions are provided below.

## Reproduce the book in Binder

To reproduce this book you can simply click on the link below to see the code running in your web browser (see details of how this works at [mybinder.org](https://mybinder.org/)):

[![Binder](http://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/geocompr/py/main?urlpath=lab/tree/ipynb)


## Reproduce the book with conda installation

### Installation on Windows

* Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) either by:
  - Downloading and running the .exe link manually, or
  - With the [command](https://community.chocolatey.org/packages/miniconda3) `choco install miniconda3` from a PowerShell terminal after installing [Chocolatey](https://chocolatey.org/install)
* Open the Anaconda Prompt (or a fresh PowerShell terminal after running the command [`conda init powershell`](https://github.com/conda/conda/issues/8428#issuecomment-474867193) from the Anaconda prompt), navigate to the above-mentioned working directory, and then run:

### Installation on Mac/Linux

Install conda, e.g. with the following commands in a Linux terminal:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
chmod +x Miniconda3-py39_4.12.0-Linux-x86_64.sh
./Miniconda3-py39_4.12.0-Linux-x86_64.sh
```
You should see prompts like this:

```
Please answer 'yes' or 'no':'
>>> yes

Miniconda3 will now be installed into this location:
/home/robin/miniconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below
```

### Create and activate conda environment

After installing conda you should be able to run the `conda create env` command above from bash to install the dependencies.

```sh
 # Warning may take several (10+) minutes to install the dependencies:
conda env create -f environment.yml
```

Activate the new environment with

```sh
conda activate geocompy # the default name of the environment
```

### Serving a local version of the book with quarto

Reproduce a live preview of the book with the following command, which reqires that you have installed [quarto](https://quarto.org/):

```sh
quarto preview # generate live preview of the book
```

### Reproducing chapters with jupyter

* Open the Jupyter Notebook of any of chapters using a command such as:

```sh
jupyter notebook 02-spatial-data.ipynb
```

### Updating packages/environments with conda

<details>

Update all packages to the latest versions as follows:

```sh
conda update --all
```


You can also install individual packages with:

```sh
conda install jupyter # for example
```

or

```sh
conda install -c conda-forge topojson # from the conda-forge channel
```

If you ever want to remove the environment, which is called `geocompy` by default, you can run the following command:

```sh
conda env remove -n geocompy
```

</details>

## Installing packages with pip

For Linux, use your preferred package manager to install the packages used in the book (`geopandas`, `rasterio`, etc.) as specified in each chapter, as well as the Jupyter Notebook interface. For example, using `pip` to install the Jupyter Notebook package is as follows:

```sh

pip install jupyter-book
```

Then, navigate to the above-mentioned working directory, and open the Jupyter Notebook of any of chapters using a command such as:

```sh
jupyter notebook 02-spatial-data.ipynb
```

You should see something like this: 

![](https://user-images.githubusercontent.com/1825120/176920562-d2e7f9af-84b4-4352-8a50-9d9946084c66.png)

See documentation on running and developing Python code in a Jupyter notebook at [docs.jupyter.org](https://docs.jupyter.org/en/latest/).

<!-- ## Reproduce the book in a Docker container with VSCode IDE -->

<!-- Todo: help wanted -->

<!-- ## Reproduce the book in a Docker container

Note: experimental.

```
docker run -it -p 8888:8888 -v $(pwd):/root geocompr/geocompr:conda
jupyter 
```

## Reproduce the book in a Docker container with RStudio IDE

```bash
docker pull geocompr/geocompr:python
# Remove the --rm below for a persistent image
docker run --rm -d -p 8784:8787 -e DISABLE_AUTH=TRUE --name geocompy \
  -v $(pwd):/home/rstudio/pytest geocompr/geocompr:python
firefox localhost:8784 # or your browser of choice
# docker kill geocompy # stop the image
```

After opening the relevant project running `quarto preview` in the system shell in browser-based IDE opened by the command above, you should see something like this where you can run code and even modify the book and see changes with the previou command.

![](https://user-images.githubusercontent.com/1825120/156414301-bfe622c5-1290-4f85-8a21-08d2a6d77df1.png) -->


