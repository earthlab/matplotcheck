# autograde
Autograding package for EA and other classes


# Earth Py

A package built to support python teaching in the Earth Lab earth analytics program
at University of Colorado, Boulder.

## Install

To install, use pip. `--upgrade` is optional but it ensures that the package overwrites
when you install and you have the current version. If you don't have the package
yet you can still use the `--upgrade` argument.

`pip install --upgrade git+https://github.com/earthlab/autograde.git`

Then import it into python.

`import autograde as gr`

## Background

This library was developed to simplify the autograding process of Matplotlib plots. Visually similar plots can be created in a variety of ways and hold different metadata. Our goal is to abstract away these differences by creating a simple way to test student plots.

Beyond that, we have noticed common groupings of assertions for specific plot types. `PlotBasicSuite`objects have been created to avoid repetition in writing out assertions, and return a TestSuite instead. To run the suite after it has been created, use a unittest text runner.

## Examples

2D plot with x-axis label containing ‘x’ and y-axis label containing ‘y’ and ‘data’
`from autograde.cases import PlotBasicSuite
import pandas as pd
import unittest
axis = plt.gca()
data = pd.DataFrame(data={“x”:xvals, “y”:yvals})
suite = PlotBasicSuite(ax=axis, data_exp=data, xcol=”x”, ycol=”y”)
xlabel_contains=[“x”], ylabel_contains = [“y”,”data”])
results = unittest.TextTestRunner().run(suite)`

Plot containing a spatial raster image and spatial polygon vector data
`from autograde.cases import PlotRasterSuite
axis = plt.gca()
suite = PlotRasterSuite(ax=axis, im_expected=image, polygons=polygons)
results = unittest.TextTestRunner().run(suite)`

If you prefer to forgo the groupings into TestSuites, you can just use the assertions instead.

2D plot with x-axis label containing ‘x’ and y-axis label containing ‘y’ and ‘data’
`from autograde.base import PlotTester
import pandas as pd
axis = plt.gca()
pt = PlotTester(axis)
data = pd.DataFrame(data={“x”:xvals, “y”:yvals})
pt.assert_xydata(data, “x”, “y”)
pt.assert_xlabel_contains([“x”])
pt.assert_ylabel_contains([“y”, “data”])`

Plot containing a spatial raster image and spatial polygon vector data
`from autograde.raster import RasterTester
From autograde.vector import VectorTester
axis = plt.gca()
rt = RasterTester(axis)
vt = VectorTester(axis)
rt.assert_image(im_expected=image)
vt.assert_polygons(polygons_expected=polygons)`

Caveats: This repo likely misses edge cases of the many ways matplotlib plots can be created. Please feel free to submit bugs!


## Contributors

- Kristen Curry

Contributing Breakers:

- Leah Wasser
