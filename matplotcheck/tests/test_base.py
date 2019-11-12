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


""" assert_string_contains Tests """


def test_assert_string_contains(pt_line_plt):
    """Tests that assert_string_contains passes with correct expected strings."""
    test_string = "this is a test string"
    string_expected = ["this", "is", "a", "test"]
    pt_line_plt.assert_string_contains(test_string, string_expected)
    plt.close()


def test_assert_string_contains_fails(pt_line_plt):
    """Tests that assert_string_contains fails with incorrect expected strings."""
    test_string = "this is a test string"
    string_expected = ["this", "is", "not", "a", "test"]
    with pytest.raises(
        AssertionError, match="String does not contain expected string: not"
    ):
        pt_line_plt.assert_string_contains(test_string, string_expected)
    plt.close()


def test_assert_string_contains_or(pt_line_plt):
    """Tests that assert_string_contains correctly passes when using OR logic."""
    test_string = "this is a test string"
    string_expected = ["this", ["is", "not"], "a", "test"]
    pt_line_plt.assert_string_contains(test_string, string_expected)
    plt.close()


def test_assert_string_contains_or_fails(pt_line_plt):
    """Tests that assert_string_contains correctly fails when using OR logic."""
    test_string = "this is a test string"
    string_expected = ["this", "is", ["not", "jambalaya"], "a", "test"]
    with pytest.raises(
        AssertionError, match="String does not contain at least one of: "
    ):
        pt_line_plt.assert_string_contains(test_string, string_expected)
    plt.close()


def test_assert_string_contains_handles_short_list_passes(pt_line_plt):
    """Tests that assert_string_contains correctly passes in the case that
    strings_expected conains a list of length 1."""
    test_string = "this is a test string"
    string_expected = [["this"], ["is"]]
    pt_line_plt.assert_string_contains(test_string, string_expected)
    plt.close()


def test_assert_string_contains_handles_short_list_fails(pt_line_plt):
    """Tests that assert_string_contains correctly fails in the case that
    strings_expected conains a list of length 1."""
    test_string = "this is a test string"
    string_expected = [["this"], ["is"], ["not"]]
    with pytest.raises(
        AssertionError, match="String does not contain expected string: not"
    ):
        pt_line_plt.assert_string_contains(test_string, string_expected)
    plt.close()


def test_assert_string_contains_passes_with_none(pt_line_plt):
    """Tests that assert_string_contains passes when strings_expected is None"""
    test_string = "this is a test string"
    string_expected = None
    pt_line_plt.assert_string_contains(test_string, string_expected)
    plt.close()


def test_assert_string_contains_passes_with_empty(pt_line_plt):
    """Tests that assert_string_contains passes when strings_expected is empty"""
    test_string = "this is a test string"
    string_expected = []
    pt_line_plt.assert_string_contains(test_string, string_expected)
    plt.close()
