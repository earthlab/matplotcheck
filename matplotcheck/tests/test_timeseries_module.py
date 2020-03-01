import pytest
from matplotcheck.base import PlotTester
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO


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
def pd_df_timeseries_csv():
    """Create a pandas dataframe for testing, with timeseries in one column,
    imported from a csv. For unknown reasons, this causes matplotlib to convert
    dates differently."""

    f = StringIO(
        """date,A
    19990430 04:00,0.10
    19990430 07:00,0.10
    19990430 08:00,0.20
    19990430 09:00,0.10
    19990430 10:00,0.10
    19990501 01:00,0.00
    """
    )

    return pd.read_csv(f, parse_dates=["date"])


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


@pytest.fixture
def pt_time_csv(pd_df_timeseries_csv):
    fig, ax = plt.subplots()

    ax.scatter(pd_df_timeseries_csv["date"], pd_df_timeseries_csv["A"])

    return PlotTester(ax)


"""TIMESERIES DATA TESTS"""


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


def test_assert_xydata_conversion(pd_df_timeseries_csv, pt_time_csv):
    """For unknown reasons, matplotlib sometimes converts dates to days since
    year 1 (instead of days since 1970). This tests that assert_xydata correctly
    passes."""

    pt_time_csv.assert_xydata(
        xy_expected=pd_df_timeseries_csv, xtime=True, xcol="date", ycol="A"
    )


def test_assert_xydata_conversion_fails(pd_df_timeseries_csv, pt_time_csv):
    """For unknown reasons, matplotlib sometimes converts dates to days since
    year 1 (instead of days since 1970). This tests that assert_xydata correctly
    fails."""

    pd_df_timeseries_csv.iloc[0, 0] = pd.Timestamp("1999-04-29 04:00:00")
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_time_csv.assert_xydata(
            xy_expected=pd_df_timeseries_csv, xtime=True, xcol="date", ycol="A"
        )
