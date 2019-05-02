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


def test_get_titles_suptitle(pt_line_plt):
    """Check that the correct suptitle gets grabbed from a figure with 2 subplots"""

    assert "My Figure Title" in pt_line_plt.get_titles()[0]


def test_title_contains_axes(pt_line_plt):
    """Check title_contains tester for axes title"""

    # Should pass if contain list is empty
    pt_line_plt.assert_title_contains([], title_type="axes")
    pt_line_plt.assert_title_contains(None, title_type="axes")

    pt_line_plt.assert_title_contains(
        ["My", "Plot", "Title"], title_type="axes"
    )

    with pytest.raises(
        AssertionError, match="Title does not contain expected text:foo"
    ):
        pt_line_plt.assert_title_contains(
            ["Title", "foo", "bar"], title_type="axes"
        )

    # Should fail if given invalid title type
    with pytest.raises(
        ValueError, match="title_type must be one of the following"
    ):
        pt_line_plt.assert_title_contains(["Title"], title_type="all")


def test_title_contains_figure(pt_line_plt, pt_bar_plt):
    """Check title_contains tester for figure title"""

    pt_line_plt.assert_title_contains(
        ["My", "Figure", "Title"], title_type="figure"
    )

    # Should fail if there is no suptitle
    with pytest.raises(
        AssertionError, match="Expected title is not displayed"
    ):
        pt_bar_plt.assert_title_contains(
            ["My", "Figure", "Title"], title_type="figure"
        )


def test_title_contains_both_axes_figure(pt_line_plt):
    """Check title_contains tester for combined axes + figure titles"""

    pt_line_plt.assert_title_contains(
        ["My", "Figure", "Plot", "Title"], title_type="either"
    )

    with pytest.raises(
        AssertionError, match="Title does not contain expected text:foo"
    ):
        pt_line_plt.assert_title_contains(
            ["My", "Figure", "Plot", "Title", "foo"], title_type="either"
        )


""" CAPTION TESTS """


def test_get_caption(pt_line_plt):
    """Make sure that get caption returns correct text string"""

    assert "Figure Caption" == pt_line_plt.get_caption().get_text()


def test_assert_caption_contains(pt_line_plt):
    """Test that caption contains passes and fails as expected"""

    pt_line_plt.assert_caption_contains([["Figure"], ["Caption"]])

    # Should pass when no strings expected
    pt_line_plt.assert_caption_contains(None)

    with pytest.raises(
        AssertionError, match="Caption does not contain expected string: foo"
    ):
        pt_line_plt.assert_caption_contains([["foo"], ["bar"]])


def test_assert_caption_contains_nocaption(pt_bar_plt):
    """Test that caption_contains fails when there is no caption"""
    with pytest.raises(
        AssertionError, match="No caption exist in appropriate location"
    ):
        pt_bar_plt.assert_caption_contains([["Figure"], ["Caption"]])
