"""
Testing Histograms
==================

These are some examples of using the basic functionality of MatPlotCheck
to test histogram plots in Python.

"""

################################################################################
# Setup
# -----
# You will start by importing the required packages and plotting a histogram.

import matplotlib.pyplot as plt
import matplotcheck.base as mpc
import matplotcheck.notebook as nb
import numpy as np


data = np.exp(np.arange(0, 5, 0.01))

fig, ax = plt.subplots()
ax.hist(data, bins=5, color="gold")

plot_1_hold = nb.convert_axes(plt, which_axes="current")

################################################################################
# Testing the Histogram
# ---------------------
# Now you can make a PlotTester object and test the histogram. We'll test both
# the number of bins and the values of those bins.

###############################################################################
#
# .. note::
#   Throughout this vignette, the term `bin value` is used to describe the
#   number of datapoints that fall within a bin. In other words, a bin's value
#   is equal to the height of the bar correspondign to that bin. For example,
#   the value of the first bin in the above histogram is 341. Note that the
#   height of the first bar is also 341.

plot_tester_1 = mpc.PlotTester(plot_1_hold)

plot_tester_1.assert_num_bins(5)

expected_bin_values = [341, 68, 40, 28, 23]
plot_tester_1.assert_bin_values(expected_bin_values)
################################################################################
# And we can also run some tests that will fail.
#
try:
    plot_tester_1.assert_num_bins(6)
except AssertionError as message:
    print("AssertionError:", message)

try:
    plot_tester_1.assert_bin_values([1, 4, 1, 3, 4])
except AssertionError as message:
    print("AssertionError:", message)

################################################################################
# Determining Expected Values
# ---------------------------
# With a histogram, you may not know the values you expect to find for each bin
# before you begin testing. (More simply, you probably know how you expect a
# histogram to look and how you expect it to be made. But you might not know
# the exact height of each bar in that histogram.) In this case, matplotcheck
# provides a method for extracting the bin values from an existing histogram:
# ``get_bin_values()``.
#
# To use this, you can create a histogram however you think it should be created
# (this will be called the expected histogram) and use it as a reference. Then
# you can extract the bin values from it (called the expected values). These
# expected values can be used to test whether another histogram (e.g. a
# student's histogram) also contains the expected values.
#
# For this example, you will start by creating a histogram that will serve as
# your expected histogram, and then extracting the expected values from it. To
# do this, you need to create a `PlotTester` object from it and use the
# ``get_bin_values()`` method.

expected_data = np.sin(np.arange(0, 2 * np.pi, np.pi / 50))

fig, ax = plt.subplots()
ax.hist(expected_data, bins=8, color="gold")

expected_plot_hold = nb.convert_axes(plt, which_axes="current")
plot_tester_expected = mpc.PlotTester(expected_plot_hold)
print(plot_tester_expected.get_bin_values())

################################################################################
# Great! Now you know the bin values that you expect to see when you test a
# plot.
#
# Now you can create another histogram (our testing histogram) and check
# whether it matches the expected histogram (i.e. check wether its bin values
# match the expected bin values).

# Create and plot the testing histogram
testing_data = np.sin(np.arange(2 * np.pi, 4 * np.pi, np.pi / 50))
fig, ax = plt.subplots()
ax.hist(testing_data, bins=8, color="orange")
testing_plot_hold = nb.convert_axes(plt, which_axes="current")

# Testing the histogram against the expected bin values
plot_tester_testing = mpc.PlotTester(testing_plot_hold)
plot_tester_testing.assert_bin_values(
    [23.0, 10.0, 8.0, 9.0, 9.0, 8.0, 10.0, 23.0]
)

################################################################################
# Since ``assert_bin_values()`` did not raise an ``AssertionError``, you know
# that the test passed. This means the testing histogram had the same bin values
# as the expected histogram.

###############################################################################
#
# .. note::
#   In this example, you have created the expected histogram and the testing
#   histogram in the same file. Normally you would create the expected histogram
#   in one location, extract the expected bin values from it, and use those to
#   test the testing histogram in another location (e.g. within a student's
#   homework assignment.)


################################################################################
# Testing with Tolerances
# -----------------------
# In some cases, you might want to run a test that doesn't require the bin
# values to match exactly. For this, you can use the ``tolerance`` argument of
# the ``assert_bin_values()`` method.
#
# You will start by making two histograms with slightly different data and
# storing the plots with ``nb.convert_axes()``. The gold plot will serve as the
# expected plot, and the orange plot will serve as the testing plot.

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
# Now you will create a `PlotTester` object for each plot. This allows you to
# extract the expected bin values from the expected plot and allows you to
# test the testing plot.

plot_tester_expected_2 = mpc.PlotTester(expected_plot_2_hold)
bins_expected_2 = plot_tester_expected_2.get_bin_values()

plot_tester_testing_2 = mpc.PlotTester(testing_plot_2_hold)

################################################################################
# You'll notice that the test (orange) plot differs somewhat from the
# expected (gold) plot, but still has a similar shape and similar bin
# values.
#
# If you test it without the ``tolerance`` argument, the assertion will fail.

try:
    plot_tester_testing_2.assert_bin_values(bins_expected_2)
except AssertionError as message:
    print("AssertionError:", message)

################################################################################
# However, if you set a tolerance, the assertion can pass. Here you will test it
# with ``tolerance=0.2``.

plot_tester_testing_2.assert_bin_values(bins_expected_2, tolerance=0.2)

################################################################################
# Because no ``AssertionError`` is raised, you know that the test passed with
# a tolerance of 0.2. However, the test will not pass with a tolerance that is
# too small; the test will fail with ``tolerance=0.1``.

try:
    plot_tester_testing_2.assert_bin_values(bins_expected_2, tolerance=0.1)
except AssertionError as message:
    print("AssertionError:", message)

###############################################################################
#
# .. note::
#   When using tolerances, the ``tolerance`` argument is taken as a relative
#   tolerance. For more information, see the documentation for the
#   ``base.assert_bin_heights()`` method.
