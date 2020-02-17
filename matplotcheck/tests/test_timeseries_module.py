import pytest
from matplotcheck.base import PlotTester
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""Fixtures"""


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
def pd_df_timeseries_low():
    """Create a pandas dataframe for testing, with timeseries in one column,
    with dates before 1970."""
    return pd.DataFrame(
        {
            "time": pd.date_range(start="1/1/1900", periods=100),
            "A": np.random.randint(0, 100, size=100),
        }
    )


@pytest.fixture
def pt_time_line_plt(pd_df_timeseries):
    """Create timeseries line plot for testing"""
    fig, ax = plt.subplots()

    pd_df_timeseries.plot("time", "A", kind="line", ax=ax)

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def pt_time_line_plt_low(pd_df_timeseries_low):
    """Create timeseries line plot for testing"""
    fig, ax = plt.subplots()

    pd_df_timeseries_low.plot("time", "A", kind="line", ax=ax)

    axis = plt.gca()

    return PlotTester(axis)


"""TIMESERIES TESTS"""


def test_assert_xydata_timeseries(pt_time_line_plt, pd_df_timeseries):
    """Tests that assert_xydata correctly passes with time data and xtime=True"""
    pt_time_line_plt.assert_xydata(
        pd_df_timeseries, xcol="time", ycol="A", xtime=True
    )
    plt.close()


def test_assert_xydata_timeseries_fails(pt_time_line_plt, pd_df_timeseries):
    """Tests that assert_xydata correctly fails with time data and xtime=True"""
    pd_df_timeseries.loc[0, "time"] = pd.Timestamp("2017-01-01")
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_time_line_plt.assert_xydata(
            pd_df_timeseries, xcol="time", ycol="A", xtime=True
        )
    plt.close()


def test_assert_xydata_timeseries_low(
    pt_time_line_plt_low, pd_df_timeseries_low
):
    """Tests that assert_xydata correctly passes with time data and xtime=True
    and with time data before 1970"""
    pt_time_line_plt_low.assert_xydata(
        pd_df_timeseries_low, xcol="time", ycol="A", xtime=True
    )
    plt.close()


def test_assert_xydata_timeseries_low_fails(
    pt_time_line_plt_low, pd_df_timeseries_low
):
    """Tests that assert_xydata correctly fails with time data and xtime=True
    and with time data before 1970"""
    pd_df_timeseries_low.loc[0, "time"] = pd.Timestamp("2017-01-01")
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_time_line_plt_low.assert_xydata(
            pd_df_timeseries_low, xcol="time", ycol="A", xtime=True
        )
    plt.close()


def test_hw_stuff():
    import os
    import matplotcheck.notebook as nb
    import matplotcheck.timeseries as mts

    f = "/Users/marty/earth-analytics/data/colorado-flood/precipitation/805333-precip-daily-1948-2013.csv"
    # f = os.path.join("data", "colorado-flood", "precipitation","805333-precip-daily-1948-2013.csv")
    precip_hourly = pd.read_csv(
        f, parse_dates=["DATE"], na_values=[999.99], index_col=["DATE"]
    )

    # Create a new dataframe with resample and rid of Nan values
    precip_daily = precip_hourly.resample(rule="D").sum()
    precip_monthly = precip_hourly.resample(rule="M").sum()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(
        precip_hourly.index.values, precip_hourly["HPCP"], color="purple"
    )

    ax.set(
        xlabel="Date",
        ylabel="Precipitation (Inches)",
        title="HW Plot 1: Hourly Precipitation - Boulder\n 1948 - 2013",
    )
    plot_1_ts = nb.convert_axes(plt, which_axes="current")
    mpc_plot_1_ts = mts.TimeSeriesTester(plot_1_ts)
    mpc_plot_1_ts.assert_xydata(
        xy_expected=precip_hourly.dropna().reset_index(),
        xtime=True,
        xcol="DATE",
        ycol="HPCP",
    )
