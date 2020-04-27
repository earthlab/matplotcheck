"""
Test Plots with Multiple Axes in Matplotcheck
=============================================

Below you will find some examples of how to use MatPlotCheck
to test Matplotlib objects with more than one axes in Python.

"""

################################################################################
# Import Packages
# ---------------
# To begin, import the libraries that you need.

import matplotcheck.base as pt
import matplotlib.pyplot as plt
import pandas as pd

###############################################################################
# Setup
# -----
# First you must create some example data to plot over multiple axes. This
# data could represent many different types of plots, such as plotting multiple
# satellite bands, plotting NDVI of multiple study sites over time, and much
# more.
# Once you have created your plot, you will create a Matplotcheck
# ``PlotTester`` object by providing each Matplotlib axes object to a unique
# ``PlotTester`` object.

# Create example data
line_1 = pd.DataFrame({"Ax 1 X Vals": [(0), (10)], "Ax 1 Y Vals": [(0), (10)]})
line_2 = pd.DataFrame({"Ax 2 X Vals": [(10), (0)], "Ax 2 Y Vals": [(0), (10)]})

# Plot the example data on two seperate Axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))

line_1.plot(ax=ax1, x="Ax 1 X Vals", y="Ax 1 Y Vals")
line_2.plot(ax=ax2, x="Ax 2 X Vals", y="Ax 2 Y Vals")

fig.suptitle("Figure Title")

ax1.set(title="Axes 1", xlabel = "Ax 1 X Vals", ylabel = "Ax 1 Y Vals")
ax2.set(title="Axes 2", xlabel = "Ax 2 X Vals", ylabel = "Ax 2 Y Vals")

# Create a Matplotcheck PlotTester object for each axes
plot_tester_1 = pt.PlotTester(ax1)
plot_tester_2 = pt.PlotTester(ax2)

###############################################################################
# Test Each Axes
# --------------
# Now that you have two ``PlotTester`` objects, one for each axes, you can run
# tests like you normally would on the plots!
#
# As shown below, both axes share the figure title. You can test for the figure
# title specifically in the ``assert_title_contains()`` function with the
# ``title_type`` argument. The default for the ``title_type`` argument is to
# check the figure and the axes title for the expected string, so make sure to
# specify if you need to!

# Testing the axes titles of both axes
plot_tester_1.assert_title_contains("Axes 1", title_type = "axes")

plot_tester_2.assert_title_contains("Axes 2", title_type = "axes")

# Testing the figure title of both axes (they share the figure title)
plot_tester_1.assert_title_contains("Figure", title_type = "figure")

plot_tester_2.assert_title_contains("Figure", title_type = "figure")

# Testing the x/y data of both axes
plot_tester_1.assert_xydata(line_1, xcol="Ax 1 X Vals", ycol="Ax 1 Y Vals")

plot_tester_2.assert_xydata(line_2, xcol="Ax 2 X Vals", ycol="Ax 2 Y Vals")

###############################################################################
#
# .. note::
#   If you are working on tests for jupyter notebooks, you can call the
#   line below to capture the student cell in a notebook. Then you can
#   use that object for testing.
#   testing_plot_2_hold = nb.convert_axes(plt, which_axes="all").
#   This returns a list that contains a PlotTester for each axes, which you can
#   access by calling an index on the list,
#   i.e. plot_tester_1 = testing_plot_2_hold[0]

################################################################################
# Access Axes Objects in a Jupyter Notebook
# -----------------------------------------
# Matplotcheck can be used to test plots in Jupyter Notebooks as well. The main
# difference is how you access the axes objects from the plot that you want to
# test. Below is an example of how you could access the axes of a plot with
# multiple axes you want to test in a Jupyter Notebook.

# First, import the Notebook module from Matplotcheck
import matplotcheck.notebook as nb

# Plot the example data on two seperate Axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))

line_1.plot(ax=ax1, x="Ax 1 X Vals", y="Ax 1 Y Vals")
line_2.plot(ax=ax2, x="Ax 2 X Vals", y="Ax 2 Y Vals")

fig.suptitle("Figure Title")

ax1.set(title="Axes 1", xlabel = "Ax 1 X Vals", ylabel = "Ax 1 Y Vals")
ax2.set(title="Axes 2", xlabel = "Ax 2 X Vals", ylabel = "Ax 2 Y Vals")

# Here is where you access the axes objects of the plot for testing.
# You can add the code line below to the end of any plot cell to store all axes
# objects created by matplotlib in that cell.
# Note that the ``which_axes`` value is set to "all". This will return all axes
# when there are more than one used, such as in this plot.
plot_test_hold = nb.convert_axes(plt, which_axes="all")

# This object can then be turned into a VectorTester object by accessing its
# indices.
plot_tester_1 = VectorTester(plot_test_hold[0])
plot_tester_2 = VectorTester(plot_test_hold[1])

# Now you can run the tests as you did earlier!
