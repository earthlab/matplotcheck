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


""" AXIS TESTS """


def test_axis_label_contains(pt_line_plt):
    """Checks for assert_axis_label_contains"""

    pt_line_plt.assert_axis_label_contains(axis="x", lst=["x", "label"])
    pt_line_plt.assert_axis_label_contains(axis="y", lst=["y"])

    # Fails when given an invalid axies
    with pytest.raises(ValueError, match="axis must be one of the following"):
        pt_line_plt.assert_axis_label_contains(axis="z", lst=["y"])

    with pytest.raises(
        AssertionError, match="x axis label does not contain expected text:foo"
    ):
        pt_line_plt.assert_axis_label_contains(axis="x", lst=["x", "foo"])


def test_axis_label_contains_blank(pt_multi_line_plt):
    """Check assert_axis_label_contains works when axis label and/or expected text is blank"""

    pt_multi_line_plt.assert_axis_label_contains(axis="x", lst=None)
    with pytest.raises(
        AssertionError, match="Expected x axis label is not displayed"
    ):
        pt_multi_line_plt.assert_axis_label_contains(axis="x", lst=["foo"])


def test_assert_lims(pt_line_plt):
    """Test for axis limit assertion, exact values"""
    pt_line_plt.assert_lims([0, 100], axis="x")
    pt_line_plt.assert_lims([0, 100], axis="y")

    with pytest.raises(AssertionError):
        pt_line_plt.assert_lims([0, 101], axis="x")
    with pytest.raises(AssertionError):
        pt_line_plt.assert_lims([0, 101], axis="y")
    with pytest.raises(AssertionError):
        pt_line_plt.assert_lims([1, 100], axis="x")
    with pytest.raises(AssertionError):
        pt_line_plt.assert_lims([1, 100], axis="y")


def test_assert_lims_range(pt_line_plt):
    """Test for axis limit assertion, accepting range of values"""
    pt_line_plt.assert_lims_range(((-5, 5), (95, 105)), axis="x")
    pt_line_plt.assert_lims_range(((-5, 5), (95, 105)), axis="y")

    # Should raise AssertionErrors
    with pytest.raises(AssertionError):
        pt_line_plt.assert_lims_range(((1, 5), (95, 105)), axis="x")
    with pytest.raises(AssertionError):
        pt_line_plt.assert_lims_range(((-5, 5), (95, 99)), axis="y")
    with pytest.raises(AssertionError):
        pt_line_plt.assert_lims_range(((-5, 5), (95, 100)), axis="y")
        pt_line_plt.assert_lims_range(((1, 5), (95, 105)), axis="y")


def test_assert_equal_xlims_ylims(pt_line_plt, pt_bar_plt):
    """Checks that axis xlims and ylims are equal, as expected"""
    pt_line_plt.assert_equal_xlims_ylims()

    # Should raise AssertionError
    pt_line_plt.ax.set_xlim((0, 99))
    with pytest.raises(AssertionError):
        pt_line_plt.assert_equal_xlims_ylims()


""" LEGEND TESTS """
