"""Tests for the base module"""
import pytest
import matplotlib.pyplot as plt


def test_line_plot(pt_line_plt):
    """Test that the line plot returns true for line but false for bar or
    scatter."""
    pt_line_plt.assert_plot_type("line")

    with pytest.raises(AssertionError):
        pt_line_plt.assert_plot_type("bar")
    with pytest.raises(AssertionError):
        pt_line_plt.assert_plot_type("scatter")
    plt.close()


def test_scatter_plot(pt_scatter_plt):
    """Test that the scatter plot returns true for line but false for bar or
    line."""
    pt_scatter_plt.assert_plot_type("scatter")

    with pytest.raises(AssertionError):
        pt_scatter_plt.assert_plot_type("bar")
    with pytest.raises(AssertionError):
        pt_scatter_plt.assert_plot_type("line")
    plt.close()


def test_bar_plot(pt_bar_plt):
    """Test that the scatter plot returns true for line but false for bar or
    line."""
    pt_bar_plt.assert_plot_type("bar")

    with pytest.raises(AssertionError):
        pt_bar_plt.assert_plot_type("scatter")
    with pytest.raises(AssertionError):
        pt_bar_plt.assert_plot_type("line")
    plt.close()


def test_options(pt_line_plt):
    """Test that a ValueError is raised if an incorrect plot type is provided.
    Should this test be unique of within a suite of tests?"""

    with pytest.raises(
        ValueError,
        match="Plot_type to test must be either: scatter, bar or line",
    ):
        pt_line_plt.assert_plot_type("foo")
    plt.close()


def test_correct_title(pt_line_plt):
    """Check that the correct plot title is grabbed from the axis object.
    Note that get_titles maintains case."""

    assert "Plot Title" in pt_line_plt.get_titles()[1]
    plt.close()


"""DATACHECK TESTS"""


def test_assert_xydata_scatter(pt_scatter_plt, pd_df):
    """Checks points in scatter plot against expected data"""
    pt_scatter_plt.assert_xydata(pd_df, xcol="A", ycol="B")
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
    pd_df["A"] = pd_df["A"].apply(str)
    pt_bar_plt.assert_xlabel_ydata(pd_df, xcol="A", ycol="B")
    plt.close()
