"""Tests for the notebook module"""

import pytest
import matplotlib
import matplotlib.pyplot as plt
from matplotcheck.base import PlotTester
import matplotcheck.notebook as nb


def test_notebook_convert_single_axes(basic_polygon_gdf):
    """Test convert single axes."""
    fig, ax = plt.subplots()
    basic_polygon_gdf.plot(ax=ax)
    store = nb.convert_axes(plt)
    with pytest.raises(AssertionError, match="Axis lines are displayed on"):
        PlotTester(store).assert_axis_off()
    plt.close()


def test_notebook_convert_multi_axes(basic_polygon_gdf):
    """Test convert multi axes."""
    fig, (ax1, ax2) = plt.subplots(1, 2)
    basic_polygon_gdf.plot(ax=ax1)
    basic_polygon_gdf.plot(ax=ax2)
    store = nb.convert_axes(plt, which_axes="all")
    for axes in store:
        with pytest.raises(
            AssertionError, match="Axis lines are displayed on"
        ):
            PlotTester(axes).assert_axis_off()
    plt.close()


def test_notebook_convert_last_axes(basic_polygon_gdf):
    """Test convert last axes."""
    fig, (ax1, ax2) = plt.subplots(1, 2)
    basic_polygon_gdf.plot(ax=ax2)
    store = nb.convert_axes(plt, which_axes="last")
    with pytest.raises(AssertionError, match="Axis lines are displayed on"):
        PlotTester(store).assert_axis_off()
    plt.close()


def test_notebook_convert_first_axes(basic_polygon_gdf):
    """Test convert first axes."""
    fig, (ax1, ax2) = plt.subplots(1, 2)
    basic_polygon_gdf.plot(ax=ax1)
    store = nb.convert_axes(plt, which_axes="first")
    with pytest.raises(AssertionError, match="Axis lines are displayed on"):
        PlotTester(store).assert_axis_off()
    plt.close()


def test_notebook_convert_axes_error(basic_polygon_gdf):
    """Test convert axes error."""
    fig, ax = plt.subplots()
    basic_polygon_gdf.plot(ax=ax)
    with pytest.raises(ValueError, match="which_axes must be one of the "):
        nb.convert_axes(plt, which_axes="error")
    plt.close()
