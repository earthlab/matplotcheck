"""
Base Plot Tester Example 2 -- Fix This Title
============================================

This is an example of using the basic functionality of MatPlotCheck.

"""

###############################################################################
# Setup
# -----
# We will start by importing the required packages. We will be using
# ``matplotlib.pyplot`` to create our plots, but any ``matplotlib`` based
# plotter (such as ``pandas.DataFrame.plot``) can be used.

import matplotlib.pyplot as plt
import matplotcheck.base as mpc
import matplotcheck.notebook as nb

###############################################################################
# Plot
# ----
# Now we'll create some data and plot it.

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
percip = [
    0.75,
    0.83,
    2.2,
    2.87,
    2.80,
    2.20,
    1.77,
    1.85,
    1.69,
    1.54,
    1.22,
    0.94,
]
fig, ax = plt.subplots()
ax.bar(months, percip, color="blue")
ax.set(
    title="Average Monthly Percipitation in Boulder, CO",
    xlabel="Month",
    ylabel="Percipitation (in)",
)
hold_axis_1 = fig.gca()

plot_1_copy = nb.convert_axes(plt, which_axes="all")
###############################################################################
# This is a section header
# ------------------------
#
# .. note::
#    In a Jupyter Notebook, a ``Matplotlib.axis.Axis`` object will not persisit
#    beyond the cell it was created in. Therefore, if you need to run tests on
#    an ```Axis`` object at the end of a Notebook, you will need to store a copy
#    of the `Axis`` object in another variable. The ``nb.convert_axes()``
#    function exists to make exactly this type of copy. It will pull ``Axes``
#    objects from the most recently created figure, regardless of what method
#    was used to create it. This can be very handy for grading students' work
#    because they can use whichever method they want to create a plot, and their
#    plot will be automatically copied and graded.
#
# Checking the plot
# -----------------
# Now we'll use matplotcheck to check the plot. We'll start by running a couple
# tests that will pass.
plot_1_copy = mpc.PlotTester(hold_axis_1)

pt1.assert_plot_type("bar")


###############################################################################
# This is a section header
# ------------------------
#
# .. note::
#    This is a note highlight.
#
# Overview text here.


###############################################################################
# Start the Vignette
# ------------------
