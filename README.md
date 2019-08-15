[![DOI](https://zenodo.org/badge/138660604.svg)](https://zenodo.org/badge/latestdoi/138660604)

# MatPlotCheck

[![Build Status](https://travis-ci.com/earthlab/matplotcheck.svg?branch=master)](https://travis-ci.com/earthlab/matplotcheck)
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


## Install

To install, use pip. `--upgrade` is optional but it ensures that the package overwrites
when you install and you have the current version. If you don't have the package
yet you can still use the `--upgrade` argument.

`pip install --upgrade matplotcheck`

Then import it into python.

`import matplotcheck as mpc`

## Background

This library was developed to simplify the autograding process of Matplotlib plots.
Visually similar plots can be created in a variety of ways and hold different metadata.
Our goal is to abstract away these differences by creating a simple way to test student plots.

Beyond that, we have noticed common groupings of assertions for specific plot types.
`PlotBasicSuite`objects have been created to avoid repetition in writing out assertions,
and return a TestSuite instead. To run the suite after it has been created, use a unittest text runner.

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
