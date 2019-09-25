"""Tests for the base module -- Data"""
import pytest
import matplotlib.pyplot as plt
import numpy as np
import random


"""DATACHECK TESTS"""


def test_assert_xydata_scatter(pt_scatter_plt, pd_df):
    """Checks points in scatter plot against expected data"""
    pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B")
    plt.close()


def test_assert_xydata_tolerance(pt_scatter_plt, pd_df):
    """Checks that slightly altered data still passes with an appropriate tolerance"""
    for i in range(len(pd_df["A"])):
        pd_df["A"][i] = pd_df["A"][i] + (np.floor(pd_df["A"][i] * 0.25))
        pd_df["B"][i] = pd_df["B"][i] + (np.floor(pd_df["B"][i] * 0.25))
    pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B", tolerence=0.5)
    plt.close()


def test_assert_xydata_tolerance_fail(pt_scatter_plt, pd_df):
    """Checks that data altered beyond the tolerance throws an assertion."""
    pd_df["A"][1] = pd_df["A"][1] * 2
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B", tolerence=0.1)
    plt.close()


def test_assert_xydata_changed_data(pt_scatter_plt, pd_df):
    """assert_xydata should fail when we change the data"""
    pd_df["B"][1] += 5
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B")
    plt.close()


def test_assert_xydata_scatter_points_only(pt_scatter_plt, pd_df):
    """Checks points in scatter plot against expected data"""
    pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B", points_only=True)
    plt.close()


def test_assert_xydata_changed_data_points_only(pt_scatter_plt, pd_df):
    """assert_xydata should fail when we change the data"""
    pd_df["B"][1] += 5
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_scatter_plt.assert_xydata(
            pd_df, xcol="A", ycol="B", points_only=True
        )
    plt.close()


'''
def test_assert_xydata_timeseries(pt_time_line_plt, pd_df_timeseries):
    """Commenting this out for now as this requires a time series data object
    this is failing because the time data needs to be in seconds like how
    mpl saves it. """
    pt_time_line_plt.assert_xydata(pd_df_timeseries, xcol='time', ycol='A', xtime=True)
'''


def test_assert_xydata_xlabel(pt_bar_plt, pd_df):
    "Tests the xlabels flag on xydata"
    pd_df["A"] = pd_df["A"].apply(str)
    pt_bar_plt.assert_xydata(pd_df, xcol="A", ycol="B", xlabels=True)
    plt.close()


def test_assert_xydata_xlabel_fails(pt_bar_plt, pd_df):
    "Tests the xlabels flag on xydata"
    pd_df["A"] = pd_df["A"].apply(str)
    pd_df.iloc[1, 0] = "this ain't it cheif"
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_bar_plt.assert_xydata(pd_df, xcol="A", ycol="B", xlabels=True)
    plt.close()


def test_assert_xydata_expected_none(pt_scatter_plt):
    "Tests that assert_xydata passes when xy_expected is None"
    pt_scatter_plt.assert_xydata(None)
    plt.close()
