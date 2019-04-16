"""Tests for the base module"""
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotcheck.base import PlotTester
from matplotcheck.raster import RasterTester


""" PYTEST FIXTURES """


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

    # Basic plot plus title, x and y axis labels
    pd_df.plot("A", "B", kind="line", ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")
    ax.set_xlim((0, 100))
    ax.set_ylim((0, 100))

    # Insert caption
    ax_position = ax.get_position()
    fig.text(
        ax_position.ymax - 0.25, ax_position.ymin - 0.075, "Figure Caption"
    )

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def multi_line_plt(pd_df):
    """Line plot with multiple data columns, plus legend"""
    fig, ax = plt.subplots()
    pd_df.plot(ax=ax)
    ax.set_ylim((0, 140))
    ax.legend(loc="center left", title="Legend", bbox_to_anchor=(1, 0.5))
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


""" PLOT TYPE TESTS """


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


""" TITLE TESTS """


def test_get_titles(pd_line_plt):
    """Check that the correct plot title is grabbed from the axis object.
    Note that get_titles maintains case."""

    assert "My Plot Title" == pd_line_plt.get_titles()[1]


def test_title_contains(pd_line_plt):
    """Check that title_contains tester passes and fails as expected"""

    pd_line_plt.assert_title_contains(["My", "Title"])

    with pytest.raises(AssertionError):
        pd_line_plt.assert_title_contains(["foo", "bar"])


""" CAPTION TESTS """


def test_get_caption(pd_line_plt):
    """Make sure that get caption returns correct text string"""

    assert "Figure Caption" == pd_line_plt.get_caption().get_text()


def test_assert_caption_contains(pd_line_plt):
    """Test that caption contains passes and fails as expected"""

    pd_line_plt.assert_caption_contains([["Figure"], ["Caption"]])

    with pytest.raises(AssertionError):
        pd_line_plt.assert_caption_contains([["foo"], ["bar"]])


""" AXIS TESTS """


def test_axis_label_contains(pd_line_plt):
    """Check that axis_label_contains tester passes and fails as expected"""

    pd_line_plt.assert_axis_label_contains(axis="x", lst=["x", "label"])
    pd_line_plt.assert_axis_label_contains(axis="y", lst=["y"])


def test_assert_lims(pd_line_plt):
    """Test for axis limit assertion, exact values"""
    pd_line_plt.assert_lims([0, 100], axis="x")
    pd_line_plt.assert_lims([0, 100], axis="y")

    with pytest.raises(AssertionError):
        pd_line_plt.assert_lims([0, 101], axis="x")
    with pytest.raises(AssertionError):
        pd_line_plt.assert_lims([0, 101], axis="y")
    with pytest.raises(AssertionError):
        pd_line_plt.assert_lims([1, 100], axis="x")
    with pytest.raises(AssertionError):
        pd_line_plt.assert_lims([1, 100], axis="y")


def test_assert_lims_range(pd_line_plt):
    """Test for axis limit assertion, accepting range of values"""
    pd_line_plt.assert_lims_range(((-5, 5), (95, 105)), axis="x")
    pd_line_plt.assert_lims_range(((-5, 5), (95, 105)), axis="y")

    # Should raise AssertionErrors
    with pytest.raises(AssertionError):
        pd_line_plt.assert_lims_range(((1, 5), (95, 105)), axis="x")
    with pytest.raises(AssertionError):
        pd_line_plt.assert_lims_range(((-5, 5), (95, 99)), axis="y")
    with pytest.raises(AssertionError):
        pd_line_plt.assert_lims_range(((-5, 5), (95, 100)), axis="y")
        pd_line_plt.assert_lims_range(((1, 5), (95, 105)), axis="y")


def test_assert_equal_xlims_ylims(pd_line_plt, pd_bar_plt):
    """Checks that axis xlims and ylims are equal, as expected"""
    pd_line_plt.assert_equal_xlims_ylims()

    # Should raise AssertionError
    pd_line_plt.ax.set_xlim((0, 99))
    with pytest.raises(AssertionError):
        pd_line_plt.assert_equal_xlims_ylims()


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
