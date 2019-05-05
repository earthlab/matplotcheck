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


def test_assert_legend_titles(pt_multi_line_plt):
    """Test for checking that legend tites are equal to given string"""
    pt_multi_line_plt.assert_legend_titles(["legend"])


def test_assert_legend_titles_not_case_sensitive(pt_multi_line_plt):
    """Check that assert_legend_titles is NOT case sensitive"""
    pt_multi_line_plt.assert_legend_titles(["LeGenD"])


def test_assert_legend_titles_bad_text(pt_multi_line_plt):
    """Check that assert_legend_titles fails with wrong text"""
    with pytest.raises(
        AssertionError,
        match="Legend subtitle does not contain expected string: foo",
    ):
        pt_multi_line_plt.assert_legend_titles(["foo"])


def test_assert_legend_titles_wrong_num(pt_multi_line_plt):
    """Check assert_legend_titles fails when expected # of titles != # of legends"""
    with pytest.raises(
        AssertionError, match="Incorrect number of legend exist"
    ):
        pt_multi_line_plt.assert_legend_titles(["legend", "legend2"])


def test_assert_legend_labels(pt_multi_line_plt):
    """Test for checking that legend labels are expected strings"""
    pt_multi_line_plt.assert_legend_labels(["a", "b"])


def test_assert_legend_not_case_sensitive(pt_multi_line_plt):
    """Check that assert_legend_labels is NOT case sensitive"""
    pt_multi_line_plt.assert_legend_labels(["A", "B"])


def test_assert_legend_labels_bad_text(pt_multi_line_plt):
    """Check that assert_legend_labels raises expected error when given wrong text"""
    with pytest.raises(
        AssertionError, match="Legend does not have expected labels"
    ):
        pt_multi_line_plt.assert_legend_labels(["a", "c"])


def test_assert_legend_labels_wrong_num(pt_multi_line_plt):
    """Check that assert_legend_labels raises expected error given wrong number of labels"""
    with pytest.raises(
        AssertionError,
        match="Legend does not contain expected number of entries",
    ):
        pt_multi_line_plt.assert_legend_labels(["a", "b", "c"])


# def test_assert_legend_no_overlay_content(pt_multi_line_plt):
#     """Test for checking whether legend overlays plot contents"""
#
#
#     pt_multi_line_plt.assert_legend_no_overlay_content()
