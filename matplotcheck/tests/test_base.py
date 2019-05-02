"""Tests for the base module"""
import pytest


""" PLOT TYPE TESTS """


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


""" TITLE TESTS """


def test_get_titles(pt_line_plt):
    """Check that the correct plot title is grabbed from the axis object.
    Note that get_titles maintains case."""

    assert "Plot Title" in pt_line_plt.get_titles()[1]


def test_get_titles_suptitle(pt_subplot_line_scatter):
    """Check that the correct suptitle gets grabbed from a figure with 2 subplots"""

    assert "Two Plot Figure" in pt_subplot_line_scatter.get_titles()[0]


def test_title_contains(pt_line_plt):
    """Check that title_contains tester passes and fails as expected"""

    pt_line_plt.assert_title_contains(["My", "Title"])

    with pytest.raises(AssertionError):
        pt_line_plt.assert_title_contains(["foo", "bar"])


""" CAPTION TESTS """


def test_get_caption(pt_line_plt):
    """Make sure that get caption returns correct text string"""

    assert "Figure Caption" == pt_line_plt.get_caption().get_text()


def test_assert_caption_contains(pt_line_plt):
    """Test that caption contains passes and fails as expected"""

    pt_line_plt.assert_caption_contains([["Figure"], ["Caption"]])

    with pytest.raises(AssertionError):
        pt_line_plt.assert_caption_contains([["foo"], ["bar"]])
