import pytest
from matplotcheck.timeseries import TimeSeriesTester
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@pytest.fixture
def pd_df_timeseries():
    """Create a pandas dataframe for testing, with timeseries in one column"""
    return pd.DataFrame(
        {
            "time": pd.date_range(start="1/1/2018", periods=100),
            "A": np.random.randint(0, 100, size=100),
        }
    )


@pytest.fixture
def pt_time_line_plt(pd_df_timeseries):
    """Create timeseries line plot for testing"""
    fig, ax = plt.subplots()
    pd_df_timeseries.plot("time", "A", kind="line", ax=ax)
    axis = plt.gca()

    return TimeSeriesTester(axis)


"""
matplotlib stores datetime data in a very... unique way. It stores everything
as the number of days since some epoch. If you plot a dataframe containing
datetime.datetime objects or pandas.Timestamp objects, it will convert it days
since epoch. Sometimes matplotlib chooses Jan 1, 1970 as the epoch. Other
times it chooses Jan 1, 0001. If your data contains time data (i.e. higher
precision than just dates), matplotlib will store it as fractional days since
epoch, down to millisecond precision (or whatever precision your data is in).
For datetime data between these epochs, sometimes it will choose to store it as
negative days since 1970, other times it will store it as positive days since
the year 0001.

matplotlib DOES provide functions for converting data from this weird format
back to datetime.datetime or pandas.Timestamp. However, these functions
always assume that the 1970 epoch was used.

matplotlib's documentation claims that negative values for datetime data are
not supported, and therefore data representing dates before 1970 are not
supported. However, matplotlib will happily plot data before 1970 and its
conversion functions will happily accept negative numbers and try to convert
them.

As you might imagine, this presents a number of issues for comparing datetime
data. Most obviously, it gets unreliable when we have to guess which epoch
matplotlib chose to use. We have tried a few different methods here: different
ways of converting the data, converting using both epochs and comparing both,
etc. All of them were pretty messy.

Additionally, there is the issue of floating point truncation error. matplotlib
stores this data with numpy.float64, which has 52 mantissa bits, or about 15
base-10 digits of accuracy. Since the number of days since epoch is often in
the tens-of-thousands, this means that matplotlib may not be able to accurately
represent data with millisecond precision. (Basically, the datatype isn't able
to store such a huge number with such small precision.) The actual available
precision will depend on the dates being used and the epoch matplotlib chooses.

So to solve these problems, we have done two things:

First, we don't bother to try to convert from matplotlib's data ourselves.
Instead, we require that instructors provide the expected data in matplotlib's
format when using assert_xydata(). The easiest way for instructors to do this
is for them to plot the data themselves, create a matplotcheck object from it,
and then extract the data using get_xy(). One weird quirk is that matplotlib
seems to consistently choose the same epoch when plotting the same dataset.
(However, we are unable to predict which epoch this will be for a given
dataset, and matplotlib's conversion functions don't always choose the same
epoch as when the data is plotted.) This solves the problem of being able to
convert the data.

Second, we use numpy.testing.assert_array_max_ulp() for comparing datetime data
(or any other type of numeric data). This method of comparison ensures that
floating-point roundoff error does not cause the assertion to erroneously fail.
However, this cannot prevent truncation error, and therefore cannot prevent a
loss of precision. Practically, what this means is that assert_xydata() cannot
tell the difference between times with differences of tens of milliseconds. If
it can't tell the difference, it will err on the side of passing.

For more info about the issues we've faced with this, take a look at PR #185
"""


def test_assert_xydata_timeseries(pt_time_line_plt):
    """Tests that assert_xydata() correctly passes with matching timeseries
    data."""
    data = pt_time_line_plt.get_xy()
    pt_time_line_plt.assert_xydata(data, xcol="x", ycol="y")


def test_assert_xydata_timeseries_fails(pt_time_line_plt):
    """Tests that assert_xydata() correctly fails without matching timeseries
    data."""
    data = pt_time_line_plt.get_xy()
    data.loc[0, "x"] = 100
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_time_line_plt.assert_xydata(data, xcol="x", ycol="y")


def test_assert_xydata_timeseries_truncation_error(
    pt_time_line_plt, pd_df_timeseries
):
    """Tests that assert_xydata() handles floating-point truncation error
    gracefully for timeseries data."""

    pt1 = pt_time_line_plt

    # Create second plottester object with slightly different time values
    # The change in values here should be small enough that it gets truncated
    # in matplotlib's conversion of datetime data
    for i in range(len(pd_df_timeseries)):
        pd_df_timeseries.loc[i, "time"] = pd_df_timeseries.loc[
            i, "time"
        ] + pd.Timedelta(1)
    fig, ax2 = plt.subplots()
    pd_df_timeseries.plot("time", "A", kind="line", ax=ax2)
    pt2 = TimeSeriesTester(ax2)

    # Test that the two datasets assert as equal
    data1 = pt1.get_xy()
    pt2.assert_xydata(data1, xcol="x", ycol="y")


def test_assert_xydata_timeseries_roundoff_error(pt_time_line_plt):
    """Tests that assert_xydata() handles floating-point roundoff error
    gracefully for timeseries data."""
    data = pt_time_line_plt.get_xy()
    data.loc[0, "x"] = data.loc[0, "x"] + 0.00000000001

    pt_time_line_plt.assert_xydata(data, xcol="x", ycol="y")
