"""
The Basics of Testing Plots
===========================

These are some examples of using the basic functionality of MatPlotCheck.

"""

################################################################################
# Setup
# -----
# You will start by importing the required packages and plotting a histogram.

import matplotlib.pyplot as plt
import matplotcheck.base as mpc
import matplotcheck.notebook as nb
import numpy as np
import pandas as pd


data = np.exp(np.arange(0, 5, 0.01))

fig, ax = plt.subplots()
ax.hist(data, bins=5, color="gold")

plot_1_hold = nb.convert_axes(plt, which_axes="current")

################################################################################
# Testing the Histogram
# ---------------------
# Now you can make a PlotTester object and test the histogram. We'll test both
# the number of bins and the heights of those bins.

plot_tester_1 = mpc.PlotTester(plot_1_hold)

plot_tester_1.assert_num_bins(5)

expected_bin_heights = [341, 68, 40, 28, 23]
plot_tester_1.assert_bin_heights(expected_bin_heights)
################################################################################
# And we can also run some tests that will fail.
#
try:
    plot_tester_1.assert_num_bins(6)
except AssertionError as message:
    print("AssertionError:", message)

try:
    plot_tester_1.assert_bin_heights([1, 4, 1, 3, 4])
except AssertionError as message:
    print("AssertionError:", message)

################################################################################
# Determining Expected Values
# ---------------------------
# With a histogram, you may not always know the heights of each bin that you
# expect to see. Instead, you might just know how to make the histogram you
# expect. In this case, matplotcheck provides a method for extracting the bin
# heights from a plot. You will start by creating a plot with unknown bin
# heights.

expected_data = np.sin(np.arange(0, 2 * np.pi, np.pi / 50))

fig, ax = plt.subplots()
ax.hist(expected_data, bins=8, color="maroon")

expected_plot_hold = nb.convert_axes(plt, which_axes="current")

################################################################################
# Now we will create a `PlotTester` object and extract the bin heights.
plot_tester_expected = mpc.PlotTester(expected_plot_hold)
print(plot_tester_expected.get_bin_heights())

################################################################################
# Great! Now that you have figured out the bin heights we expect to see, you
# can test that another plot has those same bin heights.

testing_data = np.cos(np.arange(0.5 * np.pi, 2.5 * np.pi, np.pi / 50))

fig, ax = plt.subplots()
ax.hist(testing_data, bins=8, color="pink")

testing_plot_hold = nb.convert_axes(plt, which_axes="current")

plot_tester_testing = mpc.PlotTester(testing_plot_hold)
try:
    plot_tester_testing.assert_bin_heights(
        [145.0, 64.0, 55.0, 51.0, 51.0, 54.0, 64.0, 145.0]
    )
except AssertionError as message:
    print("AssertionError:", message)
print(plot_tester_testing.get_bin_heights())
