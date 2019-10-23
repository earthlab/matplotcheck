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

###############################################################################
# Checking the plot
# -----------------
# Now we'll use matplotcheck to check the plot.
pt1 = mpc.PlotTester(hold_axis_1)

try:
    pt1.assert_plot_type("bar")
except:
    print("pt1 is not a bar plot.")
else:
    print("pt1 is a bar plot.")

try:
    pt1.assert_plot_type("line")
except:
    print("pt1 is not a line plot.")
else:
    print("pt1 is a line plot.")
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
