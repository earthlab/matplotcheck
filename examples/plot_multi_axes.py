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
# Review: The Anatomy of a Matplotlib Figure
# -------------------------------------------
#
# To understand how to test figures with subplots, you need to first
# understand the anatomy of a Matplotlib figure. A figure contains the
# figure itself and then one or more subplots. These subplots are technically
# ``matplotlib.axes`` objects.

# Create a new figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
fig.suptitle("This is a Matplotlib Figure")

ax1.set(title="Subplot 1 title (ax1 - Matplotlib.axes object)",
        xlabel="Subplot1 x Label",
        ylabel="Subplot1 y Label")

ax2.set(title="Subplot 2 title (ax2 - Matplotlib.axes object)",
        xlabel="Subplot 2 x Label",
        ylabel="Subplot 2 y Label")


# If you want to test a figure with multiple subplots, you will need to create
# a test objects for each subplot in the figure individually. You will learn
# how to do this below.


###############################################################################
# Create Example Data and Plots
# -----------------------------
# To begin, create some data to plot in your figure. You will create a
# figure with two subplots. In this example, two Pandas DataFrames are
# created to represent two different datasets. Each dataset will be plotted
# as lines in its own subplot.
#
# Once you have created your plot, you will create a Matplotcheck
# ``PlotTester`` object for each subplot using the
# ``PlotTester()`` function.

# Create example data
line_1 = pd.DataFrame({"ax1-x-values": [(0), (10)], "ax1-y-values": [(
    0), (10)]})
line_2 = pd.DataFrame({"ax2-x-values": [(10), (0)], "ax2-y-values": [(0),
                                                                    (10)]})

# Create figure that plots each dataset on it's own subplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))
fig.suptitle("Figure Title")

line_1.plot(ax=ax1, x="ax1-x-values", y="ax1-y-values")
line_2.plot(ax=ax2, x="ax2-x-values", y="ax2-y-values")


ax1.set(title="Axes 1", xlabel="Ax 1 X Vals", ylabel="Ax 1 Y Vals")
ax2.set(title="Axes 2", xlabel="Ax 2 X Vals", ylabel="Ax 2 Y Vals")

# Create Matplotcheck PlotTester object for each subplot (matplotlib.axes
# object)
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
plot_tester_1.assert_title_contains("Axes 1", title_type="axes")

plot_tester_2.assert_title_contains("Axes 2", title_type= "axes")

# Test figure title shared by both axes
plot_tester_1.assert_title_contains("Figure", title_type="figure")

plot_tester_2.assert_title_contains("Figure", title_type="figure")

# Test xy data of individual axes
plot_tester_1.assert_xydata(line_1, xcol="ax1-x-values", ycol="ax1-y-values")

plot_tester_2.assert_xydata(line_2, xcol="ax2-x-values", ycol="ax2-y-values")

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

line_1.plot(ax=ax1, x="ax1-x-values", y="ax1-y-values")
line_2.plot(ax=ax2, x="ax2-x-values", y="ax2-y-values")

fig.suptitle("Figure Title")

ax1.set(title="Axes 1", xlabel="Ax 1 X Vals", ylabel="Ax 1 Y Vals")
ax2.set(title="Axes 2", xlabel="Ax 2 X Vals", ylabel="Ax 2 Y Vals")

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
