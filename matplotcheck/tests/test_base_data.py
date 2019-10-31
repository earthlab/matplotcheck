"""Tests for the base module -- Data"""
import pytest
from matplotcheck.base import PlotTester
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


"""DATACHECK TESTS"""


def test_assert_xydata_scatter(pt_scatter_plt, pd_df):
    """Checks points in scatter plot against expected data"""
    pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B")
    plt.close()


def test_assert_xydata_tolerance(pt_scatter_plt, pd_df):
    """Checks that slightly altered data still passes with an appropriate
    tolerance"""
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


def test_assert_xydata_floatingpoint_error(pt_scatter_plt, pd_df):
    for i in range(len(pd_df["A"])):
        pd_df["A"][i] = pd_df["A"][i] + 1.0e-10
    pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B", points_only=True)


""" LABELS DATA TESTS """


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


def test_assert_xydata_xlabel_text():
    "Tests the xlabels flag on xydata works to test labels with text data"
    data = {
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "June", "July"],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    df = pd.DataFrame(data)

    fig, ax = plt.subplots()
    df.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()

    pt = PlotTester(axis)
    pt.assert_xydata(df, xcol="months", ycol="data", xlabels=True)

    plt.close()


def test_assert_xydata_xlabel_text_fails():
    "Tests the xlabels flag on xydata fails when testing labels with wrong text data"
    correct_data = {
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "June", "July"],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    plot_data = {
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "June", "Sept"],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    correct_df = pd.DataFrame(correct_data)
    plot_df = pd.DataFrame(plot_data)

    fig, ax = plt.subplots()
    plot_df.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()

    pt = PlotTester(axis)
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt.assert_xydata(correct_df, xcol="months", ycol="data", xlabels=True)

    plt.close()


def test_assert_xydata_xlabel_numeric():
    "Tests the xlabels flag on xydata works with numeric expected x-labels."
    correct_data = {
        "months": [1, 2, 3, 4, 5, 6, 7],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    plot_data = {
        "months": [1, 2, 3, 4, 5, 6, 7],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    correct_df = pd.DataFrame(correct_data)
    plot_df = pd.DataFrame(plot_data)

    fig, ax = plt.subplots()
    plot_df.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()

    pt = PlotTester(axis)
    # import pdb; pdb.set_trace()
    pt.assert_xydata(correct_df, xcol="months", ycol="data", xlabels=True)
    plt.close()


def test_assert_xydata_xlabel_numeric_fails():
    "Tests the xlabels flag on xydata correctly fails with numeric expected x-labels."
    correct_data = {
        "months": [1, 2, 3, 4, 5, 6, 7],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    plot_data = {
        "months": [1, 2, 3, 4, 5, 6, 99999],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    correct_df = pd.DataFrame(correct_data)
    plot_df = pd.DataFrame(plot_data)

    fig, ax = plt.subplots()
    plot_df.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()

    pt = PlotTester(axis)
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt.assert_xydata(correct_df, xcol="months", ycol="data", xlabels=True)
    plt.close()


def test_assert_xydata_xlabel_numeric_fails_bad_y():
    """Tests that the xlabels flag on xydata correctly fails with wrong numeric
    y-data"""
    "Tests the xlabels flag on xydata correctly fails with numeric expected x-labels."
    correct_data = {
        "months": [1, 2, 3, 4, 5, 6, 7],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    plot_data = {
        "months": [1, 2, 3, 4, 5, 6, 7],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 9999],
    }
    correct_df = pd.DataFrame(correct_data)
    plot_df = pd.DataFrame(plot_data)

    fig, ax = plt.subplots()
    plot_df.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()

    pt = PlotTester(axis)
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt.assert_xydata(correct_df, xcol="months", ycol="data", xlabels=True)
    plt.close()


def test_assert_xydata_xlabel_numeric_expected_string_actual():
    """Tests the xlabels flag on xydata correctly fails with numeric expected
    x-labels and non-numeric actial x-labels"""
    correct_data = {
        "months": [1, 2, 3, 4, 5, 6, 7],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    plot_data = {
        "months": ["1", "2", "3", "4", "5", "6", "foo"],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    correct_df = pd.DataFrame(correct_data)
    plot_df = pd.DataFrame(plot_data)

    fig, ax = plt.subplots()
    plot_df.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()

    pt = PlotTester(axis)
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt.assert_xydata(correct_df, xcol="months", ycol="data", xlabels=True)
    plt.close()


def test_assert_xydata_expected_none(pt_scatter_plt):
    "Tests that assert_xydata passes when xy_expected is None"
    pt_scatter_plt.assert_xydata(None)
    plt.close()
