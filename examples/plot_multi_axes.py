"""
Test Matplotlib Figures with SubPlots Using Matplotcheck
========================================================================

Matplotlib figures can have more than one subplot. In this vignette, you will 
learn how to use Matplotcheck to test a figure with multiple subplots. 

"""

################################################################################
# To begin, import your Python libraries.

import matplotcheck.base as pt
import matplotlib.pyplot as plt
import pandas as pd

###############################################################################
# Create Example Data and Plots
# -----------------------------
# First, you need some data to plot over multiple axes of a figure. This data
# could be satellite imagery bands, calculated values of vegetation indices
# over time for multiple sites, or any other data for which you want to create
# multiple plots within one figure. In this example, two Pandas dataframes are
# created to represent different datasets that can be plotted as individual
# line plots.
#
# Once you have created your plot, you will create a Matplotcheck
# ``PlotTester`` object for each Matplotlib axis object using the
# ``PlotTester()`` function.

# Create example data
line_1 = pd.DataFrame({"Ax 1 X Vals": [(0), (10)], "Ax 1 Y Vals": [(0), (10)]})
line_2 = pd.DataFrame({"Ax 2 X Vals": [(10), (0)], "Ax 2 Y Vals": [(0), (10)]})

# Plot example data on two separate axes
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
# Test Individual Axes Using PlotTester Objects
# ---------------------------------------------
# Now that you have two ``PlotTester`` objects, one for each axes, you can run
# tests like you normally would on the plots!
#
# In this example, both axes share the same figure title. You can test for the
# figure title specifically in the ``assert_title_contains()`` function with
# the ``title_type`` argument. The default for the ``title_type`` argument is
# to check both the figure and the axes title for the expected string, so make
# sure to specify if you need to!

# Test titles of individual axes
plot_tester_1.assert_title_contains("Axes 1", title_type = "axes")

plot_tester_2.assert_title_contains("Axes 2", title_type = "axes")

# Test figure title shared by both axes
plot_tester_1.assert_title_contains("Figure", title_type = "figure")

plot_tester_2.assert_title_contains("Figure", title_type = "figure")

# Test xy data of individual axes
plot_tester_1.assert_xydata(line_1, xcol="Ax 1 X Vals", ycol="Ax 1 Y Vals")

plot_tester_2.assert_xydata(line_2, xcol="Ax 2 X Vals", ycol="Ax 2 Y Vals")

################################################################################
# Access Axes Objects in a Jupyter Notebook
# -----------------------------------------
# Matplotcheck can be used to test plots in Jupyter Notebooks as well. The main
# difference is how you access the axes objects from the plot that you want to
# test. Below is an example of how you could access the axes of a plot with
# multiple axes you want to test in a Jupyter Notebook.

# First, import the Notebook module from Matplotcheck
import matplotcheck.notebook as nb

# Plot example data on individual axes
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
# when there is more than one axes, such as in this example figure.
plot_test_hold = nb.convert_axes(plt, which_axes="all")

# This object can then be turned into a VectorTester object by accessing its
# indices, such as [0] for the first axes of the figure.
plot_tester_1 = pt.PlotTester(plot_test_hold[0])
plot_tester_2 = pt.PlotTester(plot_test_hold[1])

# Now you can run the tests as you did earlier!
