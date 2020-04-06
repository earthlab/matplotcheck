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
