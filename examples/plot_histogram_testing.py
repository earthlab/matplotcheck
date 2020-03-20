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
import numpy as np


data = np.exp(np.arange(0, 5, 0.01))

fig, ax = plt.subplots()
ax.hist(data, bins=5, color="gold")

# If you were running this in a notebook, the commented out  line below would
# store the matplotlib object. However, in this example, you can just grab the
# axes object directly.

# plot_1_hold = nb.convert_axes(plt, which_axes="current")

################################################################################
# Testing the Histogram
# ---------------------
# Now you can make a ``PlotTester`` object and test the histogram. You'll test both
# the number of bins and the values of those bins.

###############################################################################
#
# .. note::
#   Throughout this vignette, the term `bin value` is used to describe the
#   number of datapoints that fall within a bin. In other words, a bin's value
#   is equal to the height of the bar correspondign to that bin. For example,
#   the value of the first bin in the above histogram is 341. Note that the
#   height of the first bar is also 341.

plot_tester_1 = mpc.PlotTester(ax)

plot_tester_1.assert_num_bins(5)

expected_bin_values = [341, 68, 40, 28, 23]
plot_tester_1.assert_bin_values(expected_bin_values)
################################################################################
# And you can also run some tests that will fail.
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

plot_tester_expected = mpc.PlotTester(ax)
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

# Testing the histogram against the expected bin values
plot_tester_testing = mpc.PlotTester(ax)
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
# converting the plots to ``PlotTester`` objects.

expected_data = 0.1 * np.power(np.arange(0, 10, 0.1), 2)
bins = np.arange(0, 10, 1)

fig1, ax2 = plt.subplots()
ax2.hist(expected_data, color="gold", bins=bins)

plot_tester_expected_2 = mpc.PlotTester(ax2)

################################################################################

test_data = 0.1995 * np.power(np.arange(0, 10, 0.1), 1.7)

fig2, ax2 = plt.subplots()
ax2.hist(test_data, color="orange", bins=bins)

plot_tester_testing_2 = mpc.PlotTester(ax2)

################################################################################
# With the ``PlotTester`` objects you created from the axes, you can now
# extract the expected bin values from the expected plot and test the testing
# plot.

bins_expected_2 = plot_tester_expected_2.get_bin_values()


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

################################################################################
# Testing the Histogram Midpoints
# -------------------------------
# So far, you have tested the histogram values as well as the number of bins
# the histogram has. It may also be useful to test that the data bins cover
# the range of values that they were expected to. In order to do this, you can
# test the midpoints of each bin to ensure that the data covered by each
# bin is as expected. This is tested very similarly to the bins values.
# Simply provide ``assert_bin_midpoints()`` with a list of the expected
# midpoints, and it will assert if they are accurate or not. In order to obtain
# the midpoints in a PlotTester object, you can use ``get_bin_midpoints()``,
# much like ``get_bin_values()``.
#
# For this example, you will create a plot tester object from a histogram plot,
# the same way you did for the bin values example.

fig, ax = plt.subplots()
ax.hist(testing_data, bins=8, color="gold")

plot_tester_expected_3 = mpc.PlotTester(ax)
print(plot_tester_expected_3.get_bin_midpoints())

################################################################################
# You got the values from the plot tester object! As you can see, the values
# that were collected are the midpoints for the values each histogram bin
# covers. Now you can test that they are asserted indeed correct with an
# assertion test.

try:
    plot_tester_expected_3.assert_bin_midpoints(
        [-0.875, -0.625, -0.375, -0.125, 0.125, 0.375, 0.625, 0.875]
    )
except AssertionError as message:
    print("AssertionError:", message)

################################################################################
# Here you can see that this will fail when given incorrect values.

try:
    plot_tester_expected_3.assert_bin_midpoints(
        [-0.75, -0.5, -0.25, -0, 0.25, 0.5, 0.75, 1]
    )
except AssertionError as message:
    print("AssertionError:", message)

###############################################################################
#
# .. note::
#   Keep in mind this test is for the midpoints of the range that each bin
#   covers. So if a bin covers all data that's in between 0 and 1, than the
#   value given for that bin will be .5, not 0 or 1.
