"""
Test Regression and 1:1 Lines On Plots Using Matplotcheck
===========================================================

You can use MatPlotcheck to test lines on plots. In this example you will
learn how to test that a 1:1 line or a regression line is correct as
rendered on a scatter plot.
"""

################################################################################
# To begin, import the required Python packages.

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import pandas as pd
import matplotcheck.base as pt

################################################################################
# Create Example Data
# -------------------
# Below you create some data to add to a scatter plot. You will use the
# points to calculate and create a linear regression fit line to your
# plot. You will also add a 1:1 line to your plot. This will allow you to
# compare the slope of the regression output to a standard 1:1 fit.

# Create Pandas DataFrame containing data points
col1 = list(np.random.randint(25, size=15))
col2 = list(np.random.randint(25, size=15))
data = pd.DataFrame(list(zip(col1, col2)), columns=['data1', 'data2'])

# Plot data points, regression line, and one-to-one (1:1) line for reference
fig, ax = plt.subplots()

# Use Seaborn to calculate and plot a regression line + associated points
sns.regplot('data1', 'data2',
            data=data,
            color='purple',
            ax=ax)

# Add 1:1 line to your plot
ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--', c='k')

ax.set(xlabel='data1',
       ylabel='data2',
       title='Example Data Regression Plot',
       xlim=(0, 25),
       ylim=(0, 25))

plt.show()

################################################################################
# Test Line Plots Using a matplotcheck.PlotTester Object
# ------------------------------------------------------------
# Once you have your plot, you can test the lines on the plot using
# MatPlotCheck. To begin, create a  ``matplotcheck.PlotTester``
# object. MatPlotCheck can test to see if there is a 1:1 and / or a regression
# line on your plot. It will also test that the line has the correct
# y-intercept and slope.

# Convert matplotlib plot axes object into a matplotcheck PlotTester object
line_plot_tester = pt.PlotTester(ax)

################################################################################
# Test For Regression and 1:1 Lines on a Plot
# --------------------------------------------
# You can use the method ``assert_lines_of_type()`` to test if a 1:1 or
# regression line (or both line types) are present in the plot.

# Check line types
line_plot_tester.assert_lines_of_type(line_types=['regression', 'onetoone'])

################################################################################
# Test Slope and Y Intercept
# --------------------------
# You can also test the slope and y-intercept of a line to ensure
# that the line is correct. If you made
# your line from a list of vertices, you can use the
# ``line_figure_tests.get_slope_yintercept()`` method of the PlotTester object,
# to get the slope and y-intercept. However, if you made your line
# from a regression function, it will take an extra step to get the slope and
# intercept data. In this example, ``stats.linregress`` is used to calculate
# the slope and intercept data. Once you have created that data, you can plug
# it into the ``assert_line()`` function to ensure your line in your plot has
# the correct values.

# Get slope and y intercept data of regression line for testing
slope_data, intercept_data, _, _, _ = stats.linregress(
    data.data1, data.data2)

# Check that slope and y intercept are correct (expected) values
line_plot_tester.assert_line(slope_exp=slope_data, intercept_exp=intercept_data)


################################################################################
# Test Other Aspects of the Plot
# ------------------------------
# Plots with linear regression lines and one to one lines generally have other
# important aspects to the plots aside from the lines themselves, such as the
# points the regression is based off of, or the labels of the plot. We can
# test those aspects as well to ensure they are accurate.

################################################################################
#
# .. note::
#    Matplotcheck can be used to test plots in Jupyter Notebooks as well. The main
#    difference is how you access the axes objects from the plot that you want to
#    test. Below is an example of how you could access the axes of a plot you want
#    to test in a Jupyter Notebook.

# First, import the Notebook module from Matplotcheck
import matplotcheck.notebook as nb

# Plot the data
fig, ax = plt.subplots()

# Points and regression line
sns.regplot('data1', 'data2',
            data=data,
            color='purple',
            ax=ax)

# 1:1 line
ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--', c='k')

ax.set(xlabel='data1',
       ylabel='data2',
       title='Example Data Regression Plot',
       xlim=(0, 25),
       ylim=(0, 25));

# Here is where you access the axes objects of the plot for testing.
# You can add the code line below to the end of any plot cell to store all axes
# objects created by matplotlib in that cell.
axis_object = nb.convert_axes(plt, which_axes="current")

# This object can then be turned into a PlotTester object.
line_plot_tester_2 = pt.PlotTester(axis_object)

# Now you can run the tests as you did earlier!
