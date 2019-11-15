[![DOI](https://zenodo.org/badge/138660604.svg)](https://zenodo.org/badge/latestdoi/138660604)

# MatPlotCheck
![PyPI](https://img.shields.io/pypi/v/matplotcheck.svg?color=purple&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/matplotcheck.svg?color=purple&label=pypi%20downloads&style=plastic)
![Conda](https://img.shields.io/conda/v/conda-forge/matplotcheck.svg?color=purple&style=plastic)
![Conda](https://img.shields.io/conda/dn/conda-forge/matplotcheck.svg?color=purple&label=conda-forge%20downloads&style=plastic)

[![Build Status](https://travis-ci.com/earthlab/matplotcheck.svg?branch=master)](https://travis-ci.com/earthlab/matplotcheck)
[![Build status](https://ci.appveyor.com/api/projects/status/xgf5g4ms8qhgtp21?svg=true)](https://ci.appveyor.com/project/earthlab/matplotcheck)
[![codecov](https://codecov.io/gh/earthlab/matPlotCheck/branch/master/graph/badge.svg)](https://codecov.io/gh/earthlab/matPlotCheck)
[![Documentation Status](https://readthedocs.org/projects/matplotcheck/badge/?version=latest)](https://matplotcheck.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://img.shields.io/badge/code%20style-black-000000.svg)

A package for testing different types of matplotlib plots including:

* basic matplotlib plots
* geopandas spatial vector plots
* raster plots
* time series plots
* folium plots

and more!

## Why MatPlotCheck?
There is often a need to test plots particularly when teaching data science
courses. The Matplotlib api can be complex to navigate when trying to write
tests. MatPlotCheck was developed to make it easier to test data, titles, axes
and other elements of Matplotlib plots in support of both autograding and other
testing needs.


## Install MatPlotCheck

You can install MatPlotCheck using either pip or conda.
To use pip run:

`pip install --upgrade matplotcheck`

To use conda:
`conda install -c conda-forge matplotcheck`

To import it into Python:

`import matplotcheck as mpc`


## Under Development

Matplotcheck is currently under significant development.

## Examples

2D plot with x-axis label containing "x" and y-axis label containing "y" and "data"

```python
from matplotcheck.cases import PlotBasicSuite
import pandas as pd
import unittest

axis = plt.gca()
data = pd.DataFrame(data={“x”:xvals, “y”:yvals})
suite = PlotBasicSuite(ax=axis, data_exp=data, xcol=”x”, ycol=”y”)
xlabel_contains=[“x”], ylabel_contains = [“y”,”data”])
results = unittest.TextTestRunner().run(suite)
```

### Example Plot with Spatial Raster Data

Plot containing a spatial raster image and spatial polygon vector data

```python
from matplotcheck.cases import PlotRasterSuite
axis = plt.gca()
suite = PlotRasterSuite(ax=axis, im_expected=image, polygons=polygons)
results = unittest.TextTestRunner().run(suite)
```

If you prefer to forgo the groupings into TestSuites, you can just use the assertions instead.

2D plot with x-axis label containing "x" and y-axis label containing "y" and "data"

```python
from matplotcheck.base import PlotTester
import pandas as pd
axis = plt.gca()
pt = PlotTester(axis)
data = pd.DataFrame(data={“x”:xvals, “y”:yvals})
pt.assert_xydata(data, “x”, “y”)
pt.assert_xlabel_contains([“x”])
pt.assert_ylabel_contains([“y”, “data”])
```

Plot containing a spatial raster image and spatial polygon vector data

```python
from matplotcheck.raster import RasterTester
from matplotcheck.vector import VectorTester
axis = plt.gca()
rt = RasterTester(axis)
vt = VectorTester(axis)
rt.assert_image(im_expected=image)
vt.assert_polygons(polygons_expected=polygons)
```

Caveats: This repo likely misses edge cases of the many ways matplotlib plots can be created.
Please feel free to submit bugs!


## Active Contributors

- Leah Wasser

## Dev Setup (to be moved to contributing)

setup the matplotcheck envt

```
conda env create -f environment.yml
conda activate matplotcheck-dev
```

Then setup all of the development requirements.

```
pip install -e .
pip install -r dev-requirements.txt
pre-commit install
```

## Contributors

We've welcome any and all contributions. Below are some of the
contributors to MatPlotCheck.

<a title="Ryan Solvik" href="https://www.github.com/ryla5068"><img width="60" height="60" alt="Kylen Solvik" class="pull-left" src="https://avatars.githubusercontent.com/u/43677611?size=120" /></a>
<a title="Kylen Solvik" href="https://www.github.com/ksolvik"><img width="60" height="60" alt="Kylen Solvik" class="pull-left" src="https://avatars.githubusercontent.com/u/24379590?size=120" /></a>
<a title="Kristen Curry" href="https://www.github.com/kdcurry"><img width="60" height="60" alt="Kristen Curry" class="pull-left" src="https://avatars.githubusercontent.com/u/4032126?size=120" /></a>

## How to Contribute

We welcome contributions to MatPlotCheck! Please be sure to check out our
[contributing guidelines](https://MatPlotCheck.readthedocs.io/en/latest/contributing.html)
for more information about submitting pull requests or changes to MatPlotCheck.

## License & Citation

[BSD-3](https://github.com/earthlab/matplotcheck/blob/master/LICENSE)

### Citation Information
MatPlotCheck citation information can be found on [zenodo](https://doi.org/10.5281/zenodo.2548113). A link to bibtext format is below:

*[bibtex](https://zenodo.org/record/2548114/export/hx)
