"""Tests for the base module"""
import pytest


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


""" LEGEND TESTS """


def test_assert_legend_subtitles(multi_line_plt):
    """Test for checking that legend tites are equal to given string"""
    multi_line_plt.assert_legend_titles(["legend"])

    # Requires lowercase string
    with pytest.raises(AssertionError):
        multi_line_plt.assert_legend_titles(["Legend"])
    with pytest.raises(AssertionError):
        multi_line_plt.assert_legend_labels(["legend", "legend2"])


def test_assert_legend_labels(multi_line_plt):
    """Test for checking that legend labels are expected strings"""
    multi_line_plt.assert_legend_labels(["a", "b"])

    # Require lowercase string
    with pytest.raises(AssertionError):
        multi_line_plt.assert_legend_labels(["A", "B"])
    # These should fail too
    with pytest.raises(AssertionError):
        multi_line_plt.assert_legend_labels(["a", "c"])
    with pytest.raises(AssertionError):
        multi_line_plt.assert_legend_labels(["a", "b", "c"])


# def test_assert_legend_no_overlay_content(multi_line_plt):
#     """Test for checking whether legend overlays plot contents"""
#
#
#     multi_line_plt.assert_legend_no_overlay_content()
