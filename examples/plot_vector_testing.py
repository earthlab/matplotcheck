"""
Testing Vectors with MatPlotCheck
=================================

These are some examples of using the basic functionality of MatPlotCheck
to test vector plots in Python.

"""

################################################################################
# Setup
# -----
# You will start by importing the required packages and geometry objects
# to plot and test.

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from matplotcheck.vector import VectorTester
import matplotcheck.notebook as nb
from shapely.geometry import Polygon, LineString
import numpy as np

# Create geometry objects

# Polygon GDF
coords = [(2, 4), (2, 4.25), (4.25, 4.25), (4.25, 2), (2, 2)]
coords_b = [(i[0]+5, i[1]+7) for i in coords]
polygon_a = Polygon(coords)
polygon_b = Polygon(coords_b)
polygon_gdf = gpd.GeoDataFrame(
    [1, 2], geometry=[polygon_a, polygon_b], crs="epsg:4326")


# Line GDF
linea = LineString([(1, 1), (2, 2), (3, 2), (5, 3)])
lineb = LineString([(3, 4), (5, 7), (12, 2), (10, 5), (9, 7.5)])
line_gdf = gpd.GeoDataFrame([1, 2], geometry=[linea, lineb], crs="epsg:4326")

# MultiLine GDF

linec = LineString([(2, 1), (3, 1), (4, 1), (5, 2)])
multi_line_gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(
    [line_gdf.unary_union, linec]), crs="epsg:4326")
multi_line_gdf["attr"] = ["road", "stream"]

# Point GDF

points = pd.DataFrame(
    {
        "lat": np.array([1, 2, 1, 0, 4]),
        "lon": np.array([3, 4, 0, 0, 1]),
    }
)

point_gdf = gpd.GeoDataFrame(
    {"A": np.arange(5), "B": np.arange(5)}, geometry=gpd.points_from_xy(points.lon, points.lat), crs="epsg:4326"
)
point_gdf["attr2"] = ["Tree", "Tree", "Bush", "Bush", "Bush"]

# Symbology for the legend

line_symb = {"road": "black", "stream": "blue"}
point_symb = {"Tree": "green", "Bush": "brown"}

################################################################################
# Plotting the Geometry Objects and Storing the VectorTester Object
# -----------------------------------------------------------------
# Now you can plot the geometry objects you've made. In order to plot them with
# a legend, you will have to loop through the geometry objects that have
# attributes and plot by attribute for each case.
#
# Once you've created the Matplotlib plot, you can collect the data! You
# can store the axes with the MatPlotCheck notebook function convert_axes,
# which will allow you to create the VectorTester object in a later cell.

# Collecting Vector Tester objects

fig, ax = plt.subplots()

# Plotting polygon geodataframe

polygon_gdf.plot(ax=ax, color="purple")

# Plotting line geodataframe

for ctype, lines in multi_line_gdf.groupby('attr'):
    color = line_symb[ctype]
    label = ctype
    lines.plot(color=color, ax=ax, label=label)

# Plotting point geodataframe

size = 0

for ctype, points in point_gdf.groupby('attr2'):
    color = point_symb[ctype]
    label = ctype
    size += 100
    points.plot(color=color, ax=ax, label=label, markersize=size)

# Adding legend

ax.legend(title="Legend", loc=(1.1, .1))

vector_test_plot_hold = nb.convert_axes(plt, which_axes="current")

################################################################################
# Creating the VectorTester Object
# --------------------------------
# Once you've stored the axes, you'll need to create the VectorTester object
# itself using the stored axes.

vector_test = VectorTester(vector_test_plot_hold)

###############################################################################
#
# .. note::
#   Each geometry type must be tested seperately in VectorTester. So, if your
#   plot has multiple geometry types, such as lines, polygons, and points,
#   make sure to check each geometry type seperately!

################################################################################
# Testing Legend Attributes
# -------------------------
# In addition to the legend tests available in the base module for MatPlotCheck,
# there are additional tests you can run to check vector legends, as shown
# below.

###############################################################################
#
# .. note::
#   For these tests, you can know they passed if they don't raise an
#   AssertionError. If they were to fail, they would throw an error stating
#   what went wrong.

# Check legends in doesn't overlay the plot

vector_test.assert_legend_no_overlay_content()

# If there are multiple legends, check they don't overlap.

vector_test.assert_no_legend_overlap()

################################################################################
# Testing Point Values and Geometry
# ---------------------------------
# You can check that both the position of the points and there plot values are
# accurate with the tests below. For points, you can also check that the
# size of each point varies based on it's attributes.

# Check points geometry

vector_test.assert_points(point_gdf)

# Check points plotted by type

vector_test.assert_points_grouped_by_type(point_gdf, "attr2")

# Check points size varies based on a variable.

vector_test.assert_collection_sorted_by_markersize(point_gdf, "attr2")

################################################################################
# Testing Line Values and Geometry
# --------------------------------
# Similarly to points, you can check the position and plot values of line
# geometries are accurate with the tests below.

# Check lines geometry

vector_test.assert_lines(multi_line_gdf)

# Check lines plotted by type

vector_test.assert_lines_grouped_by_type(multi_line_gdf, "attr")

################################################################################
# Testing Polygon Geometry
# ------------------------
# Currently, MatPlotCheck is unable to check that polygons were plotted by type.
# Eventually this will be supported. For the time being though, you can still
# check that polygons are plotted correctly!

# Check Polygons

vector_test.assert_polygons(polygon_gdf)
