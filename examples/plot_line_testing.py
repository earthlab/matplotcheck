"""
Testing Line Plots
==================

These are some examples of using the basic functionality of MatPlotCheck
to test line plots in Python.
"""

################################################################################
# Setup
# -----
# You will start by importing the required packages and plotting a creating
# a line plot.

import numpy as np
from scipy import stats
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotcheck.base as pt

################################################################################
# Create Example Data
# -------------------
# Before we can grade a plot we have to create example data. This data could be
# maximum lidar height readings in an area over time, or some other data
# in which you are looking for a trend over time.

# Create the data for the line plot

col1 = list(np.random.randint(25, size=15))
col2 = list(np.random.randint(25, size=15))
data = pd.DataFrame(list(zip(col1, col2)), columns=['Data1', 'Data2'])

# Plot the points, line of regression, and a one to one line for reference

fig, ax = plt.subplots()

# Points and line of regression
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

# Convert axes object into a PlotTester object

line_figure_tests = pt.PlotTester(ax)

################################################################################
# Testing the Line Plot
# ---------------------
# Now you can make a PlotTester object and test the line plot. You can test
# the line type is a one to one line or a regression line, and you can test
# that the line has the correct y intercept and slope.

################################################################################
# Testing the Line Types
# ----------------------
# As you can see, there are two line types on this plot. A one to one line for
# reference, and a regression line of the points plotted. You can use the
# function ``assert_lines_of_type()`` to test if a one to one or regression line
# (or both types of line) are present in your plot. These are the only types
# of lines you can currently test for with this function.

# Check line types
line_figure_tests.assert_lines_of_type(line_types=['regression', 'onetoone'])

################################################################################
# Testing the Slope and Y Intercept
# ---------------------------------
# Another aspect of a line plot that you can test is the slope and Y intercept,
# which checks to ensure the line has the correct values. If you made your
# line from a list of vertices, you can use the ``get_slope_yintercept()``
# function in the PlotTester object in order to get the slope and y intercept.
# However, if you made your line from a regression function, it will take an
# extra step to get the slope and intercept data. In this example,
# ``stats.linregress`` is used to calculate the slope and intercept data. Once
# you have created that data, you can plug it into the ``assert_line()``
# function to ensure your line in your plot has the correct values.

# Create the slope and intercept data for the line in the plot to check against
slope_data, intercept_data, _, _, _ = stats.linregress(
    data.Data1, data.Data2)

# Check line is correct
line_figure_tests.assert_line(slope_exp=slope_data, intercept_exp=intercept_data)


################################################################################
# Access the Axes object in a Jupyter Notebook
# --------------------------------------------
# MatPlotCheck can be used to help grade Jupyter Notebooks as well. The main
# difference is in how you would store the Axes from the plot you are grading.
# Below is an example of how you could store the Axes of a plot you are hoping
# to grade in a notebook.

# First, import the Notebook module from MatPlotCheck
import matplotcheck.notebook as nb

# Plot the data
fig, ax = plt.subplots()

# Points and line of regression
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

# HERE'S WHERE YOU STORE THE PLOT!
# This line at the end of a cell you are expecting a plot in will store any
# matplotlib plot made in that cell so you can test it at a later time.
plot_test_hold = nb.convert_axes(plt, which_axes="current")

# This can then be turned into a PlotTester object.
line_figure_tests = pt.PlotTester(plot_test_hold)

# Now you can run the tests as you did earlier!
