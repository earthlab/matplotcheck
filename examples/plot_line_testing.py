"""
Test Line Plots with Matplotcheck
=================================

These are some examples of using the basic functionality of Matplotcheck
to test line plots (including regression lines) in Python.
"""

################################################################################
# Import Packages
# ---------------
# You will start by importing the required packages and plotting a line plot.

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import pandas as pd
import matplotcheck.base as pt

################################################################################
# Create Example Data
# -------------------
# Before you create a plot, you need to create some data. For plots with
# regression lines, you will need data in which you are looking for trends
# over time, such as maximum values from lidar-derived measurements.

# Create dataframe of data points
col1 = list(np.random.randint(25, size=15))
col2 = list(np.random.randint(25, size=15))
data = pd.DataFrame(list(zip(col1, col2)), columns=['Data1', 'Data2'])

# Plot data points, regression line, and one-to-one (1:1) line for reference
fig, ax = plt.subplots()

# Points and regression line
sns.regplot('Data1', 'Data2',
            data=data,
            color='purple',
            ax=ax)

# 1:1 line
ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--', c='k')

ax.set(xlabel='Data1',
       ylabel='Data2',
       title='Example Data Regression Plot',
       xlim=(0, 25),
       ylim=(0, 25))

plt.show()

################################################################################
# Test Line Plots Using a matplotcheck.PlotTester Object
# ------------------------------------------------------------
# Now you can make a ``matplotcheck.PlotTester`` object and test the line plot. 
# You can test that the line type is a one to one line or a regression line, 
# and you can test that the line has the correct y intercept and slope.

# Convert matplotlib plot axes object into a matplotcheck PlotTester object
line_figure_tests = pt.PlotTester(ax)

################################################################################
# Test Line Types
# ---------------
# There are two line types on the plot above: a one-to-one line for
# reference and a regression line derived from the data points. You can use the method
# ``assert_lines_of_type()`` to test if a one to one or regression line
# (or both line types) are present in the plot. (NOTE: Regression and 1:1 lines are the only types
# of lines you can currently test for with this function.)

# Check line types
line_figure_tests.assert_lines_of_type(line_types=['regression', 'onetoone'])

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
    data.Data1, data.Data2)

# Check that slope and y intercept are correct (expected) values
line_figure_tests.assert_line(slope_exp=slope_data, intercept_exp=intercept_data)


################################################################################
# Access a Matplotlib Axes object in a Jupyter Notebook
# ------------------------------------------------------
# Matplotcheck can be used to test plots in Jupyter Notebooks as well. The main
# difference is how you access the axes objects from the plot that you want to
# test. Below is an example of how you could access the axes of a plot you want
# to test in a Jupyter Notebook.

# First, import the Notebook module from Matplotcheck
import matplotcheck.notebook as nb

# Plot the data
fig, ax = plt.subplots()

# Points and regression line
sns.regplot('Data1', 'Data2',
            data=data,
            color='purple',
            ax=ax)

# 1:1 line
ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--', c='k')

ax.set(xlabel='Data1',
       ylabel='Data2',
       title='Example Data Regression Plot',
       xlim=(0, 25),
       ylim=(0, 25));

# Here is where you access the axes objects of the plot for testing.
# You can add the code line below to the end of any plot cell to store all axes
# objects created by matplotlib in that cell.
plot_test_hold = nb.convert_axes(plt, which_axes="current")

# This object can then be turned into a PlotTester object.
line_figure_tests = pt.PlotTester(plot_test_hold)

# Now you can run the tests as you did earlier!
