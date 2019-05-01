"""Tests for the base module"""
import pytest
from matplotcheck.base import PlotTester


def test_line_plot(pt_line_plt):
    """Test that the line plot returns true for line but false for bar or
    scatter."""
    pt_line_plt.assert_plot_type("line")

    with pytest.raises(AssertionError):
        pt_line_plt.assert_plot_type("bar")
    with pytest.raises(AssertionError):
        pt_line_plt.assert_plot_type("scatter")


def test_scatter_plot(pt_scatter_plt):
    """Test that the scatter plot returns true for line but false for bar or
    line."""
    pt_scatter_plt.assert_plot_type("scatter")

    with pytest.raises(AssertionError):
        pt_scatter_plt.assert_plot_type("bar")
    with pytest.raises(AssertionError):
        pt_scatter_plt.assert_plot_type("line")


def test_bar_plot(pt_bar_plt):
    """Test that the scatter plot returns true for line but false for bar or
    line."""
    pt_bar_plt.assert_plot_type("bar")

    with pytest.raises(AssertionError):
        pt_bar_plt.assert_plot_type("scatter")
    with pytest.raises(AssertionError):
        pt_bar_plt.assert_plot_type("line")


def test_options(pt_line_plt):
    """Test that a ValueError is raised if an incorrect plot type is provided.
    Should this test be unique of within a suite of tests?"""

    with pytest.raises(
        ValueError,
        match="Plot_type to test must be either: scatter, bar or line",
    ):
        pt_line_plt.assert_plot_type("foo")


def test_correct_title(pt_line_plt):
    """Check that the correct plot title is grabbed from the axis object.
    Note that get_titles maintains case."""

    assert "Plot Title" in pt_line_plt.get_titles()[1]
