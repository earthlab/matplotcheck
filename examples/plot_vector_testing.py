"""
Testing Vector Plots Created Using Geopandas with MatPlotCheck
==============================================================

This vignette will show you how to use Matplotcheck to test spatial vector data
plots created using Geopandas.

"""

################################################################################
# Setup
# -----
# To begin, import the libraries that you need.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import geopandas as gpd
from matplotcheck.vector import VectorTester

# Create geometry objects

# Create a polygon GeoDataFrame
coords = [(2, 4), (2, 4.25), (4.25, 4.25), (4.25, 2), (2, 2)]
coords_b = [(i[0]+5, i[1]+7) for i in coords]
polygon_a = Polygon(coords)
polygon_b = Polygon(coords_b)
polygon_gdf = gpd.GeoDataFrame(
    [1, 2], geometry=[polygon_a, polygon_b], crs="epsg:4326")


# Create a line GeoDataFrame
linea = LineString([(1, 1), (2, 2), (3, 2), (5, 3)])
lineb = LineString([(3, 4), (5, 7), (12, 2), (10, 5), (9, 7.5)])
line_gdf = gpd.GeoDataFrame([1, 2], geometry=[linea, lineb], crs="epsg:4326")

# Create a multiline GeoDataFrame
linec = LineString([(2, 1), (3, 1), (4, 1), (5, 2)])
multi_line_gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(
    [line_gdf.unary_union, linec]), crs="epsg:4326")
multi_line_gdf["attr"] = ["road", "stream"]

# Create a point GeoDataFrame

points = pd.DataFrame(
    {
        "lat": np.array([1, 2, 1, 0, 4]),
        "lon": np.array([3, 4, 0, 0, 1]),
    }
)

point_gdf = gpd.GeoDataFrame(
    {"A": np.arange(5), "B": np.arange(5)}, geometry=gpd.points_from_xy(points.lon, points.lat), crs="epsg:4326"
)
point_gdf["size"] = [100, 100, 300, 300, 500]

# Create symbology dictionary to use in the legend

line_symb = {"road": "black", "stream": "blue"}
point_symb = {100: "purple", 300: "green", 500: "brown"}

################################################################################
# Create Your Spatial Plot
# -----------------------------------------------------------------
# Above you created several GeoPandas GeoDataFrame objects that you want
# to plot. To plot these data according to attribute value, you can group
# the geometry by attributes and plot within a loop. Once you've created
# your plot, you are ready to test it using MatPlotCheck.

# Plot your data
fig, ax = plt.subplots()
polygon_gdf.plot(ax=ax, color="purple")

# Plot your data by attributes using groupby
for ctype, lines in multi_line_gdf.groupby('attr'):
    color = line_symb[ctype]
    label = ctype
    lines.plot(color=color, ax=ax, label=label)

for ctype, points in point_gdf.groupby('size'):
    color = point_symb[ctype]
    label = ctype
    points.plot(color=color, ax=ax, label=label, markersize=ctype)

# Add a legend
ax.legend(title="Legend", loc=(1.1, .1));

# If you were running this in a notebook, the commented out  line below would
# store the matplotlib object. However, in this example, you can just grab the
# axes object directly.

# plot_1_hold = nb.convert_axes(plt, which_axes="current")

###############################################################################
#
# .. note::
#   If you are testing a plot that is created in a Jupyter Notebook - for
#   example a student assignment - and you want to get a copy of the student's
#   figure created in a cell you can use the following approach:
#   ``ax_object = nb.convert_axes(plt, which_axes="current")``
#   then in the cell below where you write your tests, you can create a
#   PlotTester object by calling:
#   ``PlotTester(ax_object)``

################################################################################
# Create A MatPlotCheck VectorTester Object
# --------------------------------
# Once you've created your plot, you can create a MatPlotCheck VectorTester object
# that can be used to test elements in the plot.

vector_test = VectorTester(ax)

###############################################################################
#
# .. note::
#   Each geometry type must be tested seperately in VectorTester. So, if your
#   plot has multiple geometry types, such as lines, polygons, and points,
#   make sure to check each geometry type separately.

###############################################################################
#
# .. note::
#   Most tests are created as assert statements. Thus, if a test fails, matplotcheck will return an error. If the test passes,
#   no message is returned.

################################################################################
# Test Point Attribute Values and Geometry xy Locations
# -------------------------------------------
# You can check that both the position of the points on the plot and the associated
# point attribute values are
# accurate using assert_points(), assert_points_grouped_by_type() and
# assert_collection_sorted_by_markersize().
#
# To check the geometry locations, you can call assert_points() and prove the
# expected points data, which in this case is the point_gdf object.
#
# If the plot uses point markers that are sized by attribute value, you can
# check that the size of each marker correctly relates to an attribute value by
# providing the geometry, point_gdf here, and the attribute the size is based
# off of, which is the 'size' column in this case.



# Check point geometry location (x, y location)
vector_test.assert_points(point_gdf)

# Check points are grouped plotted by type
vector_test.assert_points_grouped_by_type(point_gdf, "size")

# Check points size is relative to a numeric attribute value
vector_test.assert_collection_sorted_by_markersize(point_gdf, "size")

################################################################################
# Test Line Attribute Values and Coordinate Information (x, y)
# ------------------------------------------------------------
# You can also test the position and plot values of line
# geometries.

# Check line geometry
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
