"""Tests for the base module"""
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotcheck.base import PlotTester
from matplotcheck.raster import RasterTester


@pytest.fixture
def pd_df():
    """Create a pandas dataframe for testing"""
    return pd.DataFrame(
        np.random.randint(0, 100, size=(100, 2)), columns=list("AB")
    )


@pytest.fixture
def pd_scatter_plt(pd_df):
    """Create scatter plot for testing"""
    fig, ax = plt.subplots()

    pd_df.plot("A", "B", kind="scatter", ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def pd_line_plt(pd_df):
    """Create line plot for testing"""
    fig, ax = plt.subplots()

    pd_df.plot("A", "B", kind="line", ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def pd_bar_plt(pd_df):
    """Create bar plot for testing"""
    fig, ax = plt.subplots()

    pd_df.plot("A", "B", kind="bar", ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return PlotTester(axis)


def test_line_plot(pd_line_plt):
    """Test that the line plot returns true for line but false for bar or
    scatter."""
    pd_line_plt.assert_plot_type("line")

    with pytest.raises(AssertionError):
        pd_line_plt.assert_plot_type("bar")
    with pytest.raises(AssertionError):
        pd_line_plt.assert_plot_type("scatter")


def test_scatter_plot(pd_scatter_plt):
    """Test that the scatter plot returns true for line but false for bar or
    line."""
    pd_scatter_plt.assert_plot_type("scatter")

    with pytest.raises(AssertionError):
        pd_scatter_plt.assert_plot_type("bar")
    with pytest.raises(AssertionError):
        pd_scatter_plt.assert_plot_type("line")


def test_bar_plot(pd_bar_plt):
    """Test that the scatter plot returns true for line but false for bar or
    line."""
    pd_bar_plt.assert_plot_type("bar")

    with pytest.raises(AssertionError):
        pd_bar_plt.assert_plot_type("scatter")
    with pytest.raises(AssertionError):
        pd_bar_plt.assert_plot_type("line")


def test_options(pd_line_plt):
    """Test that a ValueError is raised if an incorrect plot type is provided.
    Should this test be unique of within a suite of tests?"""

    with pytest.raises(
        ValueError,
        match="Plot_type to test must be either: scatter, bar or line",
    ):
        pd_line_plt.assert_plot_type("foo")


def test_correct_title(pd_line_plt):
    """Check that the correct plot title is grabbed from the axis object.
    Note that get_titles maintains case."""

    assert "My Plot Title" == pd_line_plt.get_titles()[1]


def test_title_contains(pd_line_plt):
    """Check that title_contains tester passes and fails as expected"""

    pd_line_plt.assert_title_contains(["My", "Title"])

    with pytest.raises(AssertionError):
        pd_line_plt.assert_title_contains(["foo", "bar"])


def test_axis_label_contains(pd_line_plt):
    """Check that axis_label_contains tester passes and fails as expected"""

    pd_line_plt.assert_axis_label_contains(axis="x", lst=["x", "label"])
    pd_line_plt.assert_axis_label_contains(axis="y", lst=["y"])
