# geocompy

<https://geocompr.github.io/py/>

## Setup

Broadly, the book can be reproduced after following three steps

1. Install Quarto https://quarto.org/docs/get-started/
2. Install Jupyter, RStudio or VS Code
3. Install the Python dependencies with `miniconda3` (recommended) or Docker

Detailed instructions are provided below.

### Reproduce the book locally

For Windows, follow these steps:

* Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) either by:
  - Downloading and running the .exe link manually, or
  - With the [command](https://community.chocolatey.org/packages/miniconda3) `choco install miniconda3` from a PowerShell terminal after installing [Chocolatey](https://chocolatey.org/install)
* Open the Anaconda Prompt (or a fresh PowerShell terminal after running the command [`conda init powershell`](https://github.com/conda/conda/issues/8428#issuecomment-474867193) from the Anaconda prompt), navigate to the above-mentioned working directory, and then run:

```sh
 # Warning may take several (10+) minutes to install the dependencies:
conda env create -f environment.yml
```

Activate the new environment with

```sh
conda activate geocompy # the default name of the environment
```

Reproduce a live preview of the book with the following command, which reqires that you have installed [quarto](https://quarto.org/):

```sh
quarto preview # generate live preview of the book
```

* Open the Jupyter Notebook of any of chapters using a command such as:

```sh
jupyter notebook 02-spatial-data.ipynb
```

The above steps should also work on Linux and Mac operating systems.
Install conda, e.g. with the following commands in a Linux terminal:

```bash
bash wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh
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

After that you should be able to run the `conda create env` command above from bash to install the dependencies.

For Linux, use your preferred package manager to install the packages used in the book (`geopandas`, `rasterio`, etc.) as specified in each chapter, as well as the Jupyter Notebook interface. For example, using `pip` to install the Jupyter Notebook package is as follows:

```sh
pip install jupyter-book
```

Then, navigate to the above-mentioned working directory, and open the Jupyter Notebook of any of chapters using a command such as:

```sh
jupyter notebook 02-spatial-data.ipynb
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

### Reproduce the book in a Docker container with VSCode IDE

Todo: help wanted

### Reproduce the book in a Docker container with IPython notebook

Todo: help wanted

### Reproduce the book in a Docker container with RStudio IDE

```bash
docker pull geocompr/geocompr:python
# Remove the --rm below for a persistent image
docker run --rm -d -p 8784:8787 -e DISABLE_AUTH=TRUE --name geocompy \
  -v $(pwd):/home/rstudio/pytest geocompr/geocompr:python
firefox localhost:8784 # or your browser of choice
# docker kill geocompy # stop the image
```

After opening the relevant project running `quarto preview` in the system shell in browser-based IDE opened by the command above, you should see something like this where you can run code and even modify the book and see changes with the previou command.

![](https://user-images.githubusercontent.com/1825120/156414301-bfe622c5-1290-4f85-8a21-08d2a6d77df1.png)

### Reproduce the book in Binder

Todo: help wanted

```{bash, eval=FALSE, echo=FALSE}
# Todo: improve these instructions before showing these system commands
# To reproduce the book you need Python and and geo packages installed
# Install them through a framework such as Conda (recommended) or pip3 as follows:
pip3 install geopandas rasterio rioxarray jupyter matplotlib netcdf4 h5netcdf 
# install quarto...
quarto preview

# Run the book code on Docker:
```

