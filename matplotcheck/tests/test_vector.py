"""Tests for the vector module"""
import pytest
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotcheck.vector import VectorTester


@pytest.fixture
def poly_geo_plot(basic_polygon_gdf):
    """Create a polygon vector tester object."""
    _, ax = plt.subplots()

    basic_polygon_gdf.plot(ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def point_geo_plot(pd_gdf):
    """Create a point plot for testing"""
    fig, ax = plt.subplots()

    pd_gdf.plot(ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def bad_pd_gdf(pd_gdf):
    """Create a point geodataframe with slightly wrong values for testing"""
    return gpd.GeoDataFrame(geometry=gpd.points_from_xy(
                    pd_gdf.geometry.x + 1, pd_gdf.geometry.y + 1)
                )

def test_list_of_polygons_check(poly_geo_plot, basic_polygon):
    """Check that the polygon assert works with a list of polygons."""
    x, y = basic_polygon.exterior.coords.xy
    poly_list = [list(zip(x, y))]
    poly_geo_plot.assert_polygons(poly_list)
    plt.close()


def test_polygon_geodataframe_check(poly_geo_plot, basic_polygon_gdf):
    """Check that the polygon assert works with a polygon geodataframe"""
    poly_geo_plot.assert_polygons(basic_polygon_gdf)
    plt.close()


def test_empty_list_polygon_check(poly_geo_plot):
    """Check that the polygon assert fails an empty list."""
    with pytest.raises(ValueError, match="Empty list or GeoDataFrame "):
        poly_geo_plot.assert_polygons([])
        plt.close()


def test_empty_list_entry_polygon_check(poly_geo_plot):
    """Check that the polygon assert fails a list with an empty entry."""
    with pytest.raises(ValueError, match="Empty list or GeoDataFrame "):
        poly_geo_plot.assert_polygons([[]])
        plt.close()


def test_empty_gdf_polygon_check(poly_geo_plot):
    """Check that the polygon assert fails an empty GeoDataFrame."""
    with pytest.raises(ValueError, match="Empty list or GeoDataFrame "):
        poly_geo_plot.assert_polygons(gpd.GeoDataFrame([]))
        plt.close()


def test_polygon_dec_check(poly_geo_plot, basic_polygon):
    """
    Check that the polygon assert passes when the polygon is off by less than
    the maximum decimal precision.
    """
    x, y = basic_polygon.exterior.coords.xy
    poly_list = [[(x[0] + 0.1, x[1]) for x in list(zip(x, y))]]
    poly_geo_plot.assert_polygons(poly_list, dec=1)
    plt.close()


def test_polygon_dec_check_fail(poly_geo_plot, basic_polygon):
    """
    Check that the polygon assert fails when the polygon is off by more than
    the maximum decimal precision.
    """
    with pytest.raises(AssertionError, match="Incorrect Polygon"):
        x, y = basic_polygon.exterior.coords.xy
        poly_list = [(x[0] + 0.5, x[1]) for x in list(zip(x, y))]
        poly_geo_plot.assert_polygons(poly_list, dec=1)
        plt.close()


def test_polygon_custom_fail_message(poly_geo_plot, basic_polygon):
    """Check that the corrct error message is raised when polygons fail"""
    with pytest.raises(AssertionError, match="Test Message"):
        x, y = basic_polygon.exterior.coords.xy
        poly_list = [(x[0] + 0.5, x[1]) for x in list(zip(x, y))]
        poly_geo_plot.assert_polygons(poly_list, m="Test Message")
        plt.close()


def test_point_geometry_pass(point_geo_plot, pd_gdf):
    """Check that the point geometry test recognizes correct points."""
    point_geo_plot.assert_points(points_expected=pd_gdf)


def test_point_geometry_fail(point_geo_plot, bad_pd_gdf):
    """Check that the point geometry test recognizes incorrect points."""
    with pytest.raises(AssertionError, match="Incorrect Point Data"):
        point_geo_plot.assert_points(points_expected=bad_pd_gdf)


def test_assert_point_fails_list(point_geo_plot, pd_gdf):
    """
    Check that the point geometry test fails anything that's not a
    GeoDataFrame
    """
    list_geo = [list(pd_gdf.geometry.x), list(pd_gdf.geometry.y)]
    with pytest.raises(ValueError, match="points_expected is not expected"):
        point_geo_plot.assert_points(points_expected=list_geo)

def test_get_points(point_geo_plot, pd_gdf):
    """Tests that get_points returns correct values"""
    xy_values = point_geo_plot.get_points()
    assert(list(sorted(xy_values.x)) == sorted(list(pd_gdf.geometry.x)))
    assert(list(sorted(xy_values.y)) == sorted(list(pd_gdf.geometry.y)))


def test_assert_points_custom_message(point_geo_plot, bad_pd_gdf):
    """Tests that a custom error message is passed."""
    message = "Test message"
    with pytest.raises(AssertionError, match="Test message"):
        point_geo_plot.assert_points(points_expected=bad_pd_gdf, m=message)
