"""Tests for the base module that check data"""
import pytest
from matplotcheck.base import PlotTester
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


"""Fixtures"""


@pytest.fixture
def pd_df_monthly_data():
    """Create a pandas dataframe with monthy data"""
    monthly_data = {
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    return pd.DataFrame(monthly_data)


@pytest.fixture
def pt_monthly_data(pd_df_monthly_data):
    """Create a PlotTester object from a bar plot with monthly data"""
    fig, ax = plt.subplots()

    pd_df_monthly_data.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()
    return PlotTester(axis)


@pytest.fixture
def pd_df_monthly_data_numeric():
    """Create a pandas dataframe with monthly data and numeric month labels"""
    monthly_data = {
        "months": [1, 2, 3, 4, 5, 6, 7],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }
    return pd.DataFrame(monthly_data)


@pytest.fixture
def pt_monthly_data_numeric(pd_df_monthly_data_numeric):
    """Create a PlotTester object from a bar plot with monthly data and numeric
    month labels"""
    fig, ax = plt.subplots()

    pd_df_monthly_data_numeric.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()
    return PlotTester(axis)


@pytest.fixture
def pt_hist():
    dataframe_a = pd.DataFrame({"A": np.exp(np.arange(1, 2, 0.01))})
    bins = [2, 3, 4, 5, 6, 7, 8]
    plt.hist(dataframe_a["A"], bins=bins, alpha=0.5, color="seagreen")
    axis = plt.gca()
    return PlotTester(axis)


@pytest.fixture
def pt_hist_overlapping():
    dataframe_a = pd.DataFrame({"A": np.exp(np.arange(1, 2, 0.01))})
    dataframe_b = pd.DataFrame(
        {"B": (7.4 - (np.exp(np.arange(1, 2, 0.01)) - np.e))}
    )
    bins = [2, 3, 4, 5, 6, 7, 8]

    plt.hist(dataframe_a["A"], bins=bins, alpha=0.5, color="seagreen")
    plt.hist(dataframe_b["B"], bins=bins, alpha=0.5, color="coral")
    axis = plt.gca()
    return PlotTester(axis)


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
    """Tests the assert_xydata correctly handles floating point error"""
    for i in range(len(pd_df["A"])):
        pd_df["A"][i] = pd_df["A"][i] + 1.0e-10
    pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B", points_only=True)
    plt.close()


""" LABELS DATA TESTS """


def test_assert_xydata_xlabel(pt_bar_plt, pd_df):
    """Tests the xlabels flag on xydata"""
    pd_df["A"] = pd_df["A"].apply(str)
    pt_bar_plt.assert_xydata(pd_df, xcol="A", ycol="B", xlabels=True)
    plt.close()


def test_assert_xydata_xlabel_fails(pt_bar_plt, pd_df):
    """Tests the xlabels flag on xydata"""
    pd_df["A"] = pd_df["A"].apply(str)
    pd_df.iloc[1, 0] = "this ain't it cheif"
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_bar_plt.assert_xydata(pd_df, xcol="A", ycol="B", xlabels=True)
    plt.close()


def test_assert_xydata_xlabel_text(pd_df_monthly_data, pt_monthly_data):
    """Tests the xlabels flag on xydata works to test labels with text data"""

    pt_monthly_data.assert_xydata(
        pd_df_monthly_data, xcol="months", ycol="data", xlabels=True
    )
    plt.close()


def test_assert_xydata_xlabel_text_fails(pd_df_monthly_data, pt_monthly_data):
    """Tests the xlabels flag on xydata fails when testing labels with wrong
    text data"""

    pd_df_expected_data = pd_df_monthly_data
    pd_df_expected_data.loc[6, "months"] = "Aug"

    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_monthly_data.assert_xydata(
            pd_df_expected_data, xcol="months", ycol="data", xlabels=True
        )

    plt.close()


def test_assert_xydata_xlabel_numeric(
    pd_df_monthly_data_numeric, pt_monthly_data_numeric
):
    """Tests the xlabels flag on xydata works with numeric expected x-labels."""

    pt_monthly_data_numeric.assert_xydata(
        pd_df_monthly_data_numeric, xcol="months", ycol="data", xlabels=True
    )
    plt.close()


def test_assert_xydata_xlabel_numeric_fails(
    pd_df_monthly_data_numeric, pt_monthly_data_numeric
):
    """Tests the xlabels flag on xydata correctly fails with numeric expected
    x-labels."""

    pd_df_expected_data = pd_df_monthly_data_numeric
    pd_df_expected_data.loc[6, "months"] = 99999

    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_monthly_data_numeric.assert_xydata(
            pd_df_expected_data, xcol="months", ycol="data", xlabels=True
        )
    plt.close()


def test_assert_xydata_xlabel_numeric_fails_bad_y(
    pd_df_monthly_data_numeric, pt_monthly_data_numeric
):
    """Tests that the xlabels flag on xydata correctly fails with wrong numeric
    y-data"""

    pd_df_expected_data = pd_df_monthly_data_numeric
    pd_df_expected_data.loc[6, "data"] = 99999

    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt_monthly_data_numeric.assert_xydata(
            pd_df_expected_data, xcol="months", ycol="data", xlabels=True
        )
    plt.close()


def test_assert_xydata_xlabel_numeric_expected_string_actual(
    pd_df_monthly_data_numeric,
):
    """Tests the xlabels flag on xydata correctly fails with numeric expected
    x-labels and non-numeric actual x-labels"""

    plot_data = {
        "months": ["1", "2", "3", "4", "5", "6", "foo"],
        "data": [0.635, 0.795, 1.655, 3.085, 2.64, 1.44, 1.02],
    }

    plot_df = pd.DataFrame(plot_data)
    fig, ax = plt.subplots()
    plot_df.plot("months", "data", kind="bar", ax=ax)
    axis = plt.gca()

    pt = PlotTester(axis)
    with pytest.raises(AssertionError, match="Incorrect data values"):
        pt.assert_xydata(
            pd_df_monthly_data_numeric,
            xcol="months",
            ycol="data",
            xlabels=True,
        )
    plt.close()


def test_assert_xydata_expected_none(pt_scatter_plt):
    """Tests that assert_xydata passes when xy_expected is None"""
    pt_scatter_plt.assert_xydata(None)
    plt.close()


"""Histogram Tests"""


def test_assert_num_bins(pt_hist):
    """Tests that assert_num_bins() correctly passes"""
    pt_hist.assert_num_bins(6)

    plt.close()


def test_assert_num_bins_incorrect(pt_hist):
    """Tests that assert_num_bins() correctly fails"""
    with pytest.raises(
        AssertionError, match="Expected 5 bins in histogram, instead found 6."
    ):
        pt_hist.assert_num_bins(5)

    plt.close()


def test_assert_num_bins_double_histogram(pt_hist_overlapping):
    """Tests that assert_num_bins correctly passes with overlapping
    histograms"""
    pt_hist_overlapping.assert_num_bins(6)

    plt.close()


def test_assert_num_bins_double_histogram_incorrect(pt_hist_overlapping):
    """Tests that assert_num_bins() correctly fails with overlapping
    histograms"""
    with pytest.raises(
        AssertionError, match="Expected 5 bins in histogram, instead found 6."
    ):
        pt_hist_overlapping.assert_num_bins(5)

    plt.close()


def test_get_bin_values(pt_hist):
    """Tests that get_bin_values() returns the correct bin valuess."""
    bin_values = pt_hist.get_bin_values()
    assert bin_values == [10.0, 29.0, 22.0, 19.0, 15.0, 5.0]

    plt.close()


def test_get_bin_values_overlapping(pt_hist_overlapping):
    """Tests that get_bin_values returns the correct bin values with
    overlapping histograms"""
    bin_values = pt_hist_overlapping.get_bin_values()
    assert bin_values == [
        10.0,
        29.0,
        22.0,
        19.0,
        15.0,
        5.0,
        3.0,
        15.0,
        18.0,
        22.0,
        28.0,
        14.0,
    ]

    plt.close()


def test_assert_bin_values(pt_hist_overlapping):
    """Tests that assert_bin_values() correctly passes with overlapping
    histograms"""
    bin_values = pt_hist_overlapping.get_bin_values()

    pt_hist_overlapping.assert_bin_values(bin_values)

    plt.close()


def test_assert_bin_values_incorrect(pt_hist_overlapping):
    """Tests that assert_bin_values() correctly fails with overlapping
    histograms"""
    bin_values = pt_hist_overlapping.get_bin_values()
    bin_values[0] += 1

    with pytest.raises(
        AssertionError, match="Did not find expected bin values in plot"
    ):
        pt_hist_overlapping.assert_bin_values(bin_values)

    plt.close()


def test_assert_bin_values_tolerance(pt_hist_overlapping):
    """Test that assert_bin_values correctly passes when using tolerance
    flag."""
    bin_values = pt_hist_overlapping.get_bin_values()
    for i in range(len(bin_values)):
        bin_values[i] = bin_values[i] * 1.1

    pt_hist_overlapping.assert_bin_values(bin_values, tolerance=0.11)

    plt.close()


def test_assert_bin_values_tolerance_fails(pt_hist_overlapping):
    """Test that assert_bin_values correctly fails when using tolerance
    flag."""
    bin_values = pt_hist_overlapping.get_bin_values()
    for i in range(len(bin_values)):
        bin_values[i] = bin_values[i] * 1.1

    with pytest.raises(
        AssertionError, match="Did not find expected bin values in plot"
    ):
        pt_hist_overlapping.assert_bin_values(bin_values, tolerance=0.09)

    plt.close()
