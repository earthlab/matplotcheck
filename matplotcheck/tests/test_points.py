"""Tests for the vector module"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pytest
import geopandas as gpd

from matplotcheck.vector import VectorTester

matplotlib.use("Agg")


@pytest.fixture
def bad_pd_gdf(pd_gdf):
    """Create a point geodataframe with slightly wrong values for testing"""
    return gpd.GeoDataFrame(
        geometry=gpd.points_from_xy(
            pd_gdf.geometry.x + 1, pd_gdf.geometry.y + 1
        )
    )


@pytest.fixture
def origin_pt_gdf(pd_gdf):
    """Create a point geodataframe to test assert_points when a point at the
    origin of the plot (0, 0) is present in the dataframe. This checks
    for a specific bug fix that was added to the assert_points function."""
    origin_pt_gdf = pd_gdf.append(
        gpd.GeoDataFrame(geometry=gpd.points_from_xy([0], [0]))
    )
    origin_pt_gdf.reset_index(inplace=True, drop=True)
    return origin_pt_gdf


@pytest.fixture
def pt_geo_plot(pd_gdf):
    """Create a geo plot for testing"""
    _, ax = plt.subplots()
    size = 0
    point_symb = {"Tree": "green", "Bush": "brown"}

    for ctype, points in pd_gdf.groupby("attr"):
        color = point_symb[ctype]
        label = ctype
        size += 100
        points.plot(color=color, ax=ax, label=label, markersize=size)

    ax.legend(title="Legend", loc=(1.1, 0.1))

    return VectorTester(ax)


@pytest.fixture
def pt_geo_plot_bad(pd_gdf):
    """Create a geo plot for testing"""
    _, ax = plt.subplots()

    pd_gdf.plot(ax=ax)

    return VectorTester(ax)


@pytest.fixture
def pt_geo_plot_origin(origin_pt_gdf, two_line_gdf):
    """Create a point plot for testing assert_points with a point at the
    origin"""
    _, ax = plt.subplots()

    origin_pt_gdf.plot(ax=ax)

    two_line_gdf.plot(ax=ax)

    return VectorTester(ax)


def test_points_sorted_by_markersize_pass(pt_geo_plot, pd_gdf):
    """Tests that points are plotted as different sizes based on an attribute
    value passes"""
    pt_geo_plot.assert_collection_sorted_by_markersize(pd_gdf, "attr")
    plt.close("all")


def test_points_sorted_by_markersize_fail(pt_geo_plot_bad, pd_gdf):
    """Tests that points are plotted as different sizes based on an attribute
    value fails"""
    with pytest.raises(AssertionError, match="Markersize not based on"):
        pt_geo_plot_bad.assert_collection_sorted_by_markersize(pd_gdf, "attr")
        plt.close("all")


def test_points_grouped_by_type(pt_geo_plot, pd_gdf):
    """Tests that points grouped by type passes"""
    pt_geo_plot.assert_points_grouped_by_type(pd_gdf, "attr")
    plt.close("all")


def test_points_grouped_by_type_fail(pt_geo_plot_bad, pd_gdf):
    """Tests that points grouped by type passes"""
    with pytest.raises(AssertionError, match="Point attributes not accurate"):
        pt_geo_plot_bad.assert_points_grouped_by_type(pd_gdf, "attr")
        plt.close("all")


def test_point_geometry_pass(pt_geo_plot, pd_gdf):
    """Check that the point geometry test recognizes correct points."""
    pt_geo_plot.assert_points(points_expected=pd_gdf)
    plt.close("all")


def test_point_geometry_fail(pt_geo_plot, bad_pd_gdf):
    """Check that the point geometry test recognizes incorrect points."""
    with pytest.raises(AssertionError, match="Incorrect Point Data"):
        pt_geo_plot.assert_points(points_expected=bad_pd_gdf)
        plt.close("all")


def test_assert_point_fails_list(pt_geo_plot, pd_gdf):
    """
    Check that the point geometry test fails anything that's not a
    GeoDataFrame
    """
    list_geo = [list(pd_gdf.geometry.x), list(pd_gdf.geometry.y)]
    with pytest.raises(ValueError, match="points_expected is not expected"):
        pt_geo_plot.assert_points(points_expected=list_geo)
        plt.close("all")


def test_get_points(pt_geo_plot, pd_gdf):
    """Tests that get_points returns correct values"""
    xy_values = pt_geo_plot.get_points()
    assert list(sorted(xy_values.x)) == sorted(list(pd_gdf.geometry.x))
    assert list(sorted(xy_values.y)) == sorted(list(pd_gdf.geometry.y))
    plt.close("all")


def test_assert_points_custom_message(pt_geo_plot, bad_pd_gdf):
    """Tests that a custom error message is passed."""
    message = "Test message"
    with pytest.raises(AssertionError, match="Test message"):
        pt_geo_plot.assert_points(points_expected=bad_pd_gdf, m=message)
        plt.close("all")


def test_wrong_length_points_expected(pt_geo_plot, pd_gdf, bad_pd_gdf):
    """Tests that error is thrown for incorrect length of a gdf"""
    with pytest.raises(AssertionError, match="points_expected's length does "):
        pt_geo_plot.assert_points(bad_pd_gdf.append(pd_gdf), "attr")
        plt.close("all")


def test_convert_length_function_error(pt_geo_plot):
    """Test that the convert length function throws an error when given
    incorrect inputs"""
    with pytest.raises(ValueError, match="Input array length is not: 1 or 9"):
        pt_geo_plot._convert_length(np.array([1, 2, 3, 4]), 9)


def test_point_gdf_with_point_at_origin(pt_geo_plot_origin, origin_pt_gdf):
    """Test that assert_points works when there's a point at the origin in the
    gdf"""
    pt_geo_plot_origin.assert_points(origin_pt_gdf)
