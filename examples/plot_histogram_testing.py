"""
Testing Histograms
==================

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
# heights from a plot.
#
# To use this, you will start by creating a plot with unknown bin heights. This
# will serve as a reference; this is how we expect our histogram to look. Then
# you will store this plot in ``expected_plot_hold``.

expected_data = np.sin(np.arange(0, 2 * np.pi, np.pi / 50))

fig, ax = plt.subplots()
ax.hist(expected_data, bins=8, color="gold")

expected_plot_hold = nb.convert_axes(plt, which_axes="current")

################################################################################
# Now that you have our expected plot, or reference plot, you will need create a
# `PlotTester` object. This will allow you to extract the bin heights from the
# expected plot.

plot_tester_expected = mpc.PlotTester(expected_plot_hold)
print(plot_tester_expected.get_bin_heights())

################################################################################
# Great! Now you know the bin heights that you expect to see in a plot that you
# are testing.
#
# Now you will create another histogram and then test it against your expected
# bin heights.

# Create and plot histogram to be tested
testing_data = np.sin(np.arange(2 * np.pi, 4 * np.pi, np.pi / 50))
fig, ax = plt.subplots()
ax.hist(testing_data, bins=8, color="orange")
testing_plot_hold = nb.convert_axes(plt, which_axes="current")

# Testing the histogram against the expected bin heights
plot_tester_testing = mpc.PlotTester(testing_plot_hold)
plot_tester_testing.assert_bin_heights(
    [23.0, 10.0, 8.0, 9.0, 9.0, 8.0, 10.0, 23.0]
)

################################################################################
# Since this did not raise an ``AssertionError``, you know that the test passed,
# as expected. The plot you tested has the same bin heights as you expected.

################################################################################
# Testing with tolerances
# -----------------------
# In some cases, you might want to run a test that doesn't require the bin
# heights to match exactly. Here you can use the tolerance flag.
#
# You will start by making two histograms with slightly different data and
# storing the plots with ``nb.convert_axes()``.
expected_data = 0.1 * np.power(np.arange(0, 10, 0.1), 2)
bins = np.arange(0, 10, 1)

fig1, ax2 = plt.subplots()
ax2.hist(expected_data, color="gold", bins=bins)

expected_plot_2_hold = nb.convert_axes(plt, which_axes="current")

################################################################################

test_data = 0.1995 * np.power(np.arange(0, 10, 0.1), 1.7)

fig2, ax2 = plt.subplots()
ax2.hist(test_data, color="orange", bins=bins)

testing_plot_2_hold = nb.convert_axes(plt, which_axes="current")

################################################################################
# Now you will extract the expected bin heights from the expected plot and make a
# `PlotTester` object from the testing plot.

plot_tester_expected_2 = mpc.PlotTester(expected_plot_2_hold)
bins_expected_2 = plot_tester_expected_2.get_bin_heights()

plot_tester_testing_2 = mpc.PlotTester(testing_plot_2_hold)

################################################################################
# You'll notice that the test (orange) plot differs somewhat from the
# expected (gold) plot, but still has a similar shape and similar bin
# heights.
#
# If you test it normally, the assertion will fail.

try:
    plot_tester_testing_2.assert_bin_heights(bins_expected_2)
except AssertionError as message:
    print("AssertionError:", message)

################################################################################
# However, if you set a tolerance, the assertion can pass. Here you will test it
# with a tolerance of 0.2.

plot_tester_testing_2.assert_bin_heights(bins_expected_2, tolerance=0.2)

################################################################################
# Because no ``AssertionError`` is raised, you know that the test passed with
# a tolerance of 0.2. However, the test will not pass with a tolerance that is
# too small. Here, you see that the test will fail with a tolerance of 0.02.

try:
    plot_tester_testing_2.assert_bin_heights(bins_expected_2, tolerance=0.02)
except AssertionError as message:
    print("AssertionError:", message)

################################################################################
#  When using tolerances, the ``tolerance`` argument is taken as a relative
# tolerance. For more information, see the documentation for the
# ``base.assert_bin_heights()`` method.
