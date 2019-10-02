"""Tests for the base module"""
import pytest
import matplotlib.pyplot as plt


def test_line_plot(pt_line_plt):
    """Test that the line plot returns true for line but false for bar or
    scatter."""
    pt_line_plt.assert_plot_type("line")

    with pytest.raises(AssertionError, match="Plot is not of type bar"):
        pt_line_plt.assert_plot_type("bar")
    with pytest.raises(AssertionError, match="Plot is not of type scatter"):
        pt_line_plt.assert_plot_type("scatter")
    plt.close()


def test_scatter_plot(pt_scatter_plt):
    """Test that the scatter plot returns true for line but false for bar or
    line."""
    pt_scatter_plt.assert_plot_type("scatter")

    with pytest.raises(AssertionError, match="Plot is not of type bar"):
        pt_scatter_plt.assert_plot_type("bar")
    with pytest.raises(AssertionError, match="Plot is not of type line"):
        pt_scatter_plt.assert_plot_type("line")
    plt.close()


def test_bar_plot(pt_bar_plt):
    """Test that the scatter plot returns true for line but false for bar or
    line."""
    pt_bar_plt.assert_plot_type("bar")

    with pytest.raises(AssertionError, match="Plot is not of type scatter"):
        pt_bar_plt.assert_plot_type("scatter")
    with pytest.raises(AssertionError, match="Plot is not of type line"):
        pt_bar_plt.assert_plot_type("line")
    plt.close()


def test_options(pt_line_plt):
    """Test that a ValueError is raised if an incorrect plot type is
    provided."""

    with pytest.raises(
        ValueError,
        match="Plot_type to test must be either: scatter, bar or line",
    ):
        pt_line_plt.assert_plot_type("foo")
    plt.close()
