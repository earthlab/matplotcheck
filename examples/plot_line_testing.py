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
