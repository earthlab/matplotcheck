"""Tests for the vector module"""
import matplotlib
import matplotlib.pyplot as plt
import pytest
import geopandas as gpd
from shapely.geometry import Polygon

from matplotcheck.vector import VectorTester

matplotlib.use("Agg")


@pytest.fixture
def multi_polygon_gdf(basic_polygon):
    """
    A GeoDataFrame containing the basic polygon geometry.
    Returns
    -------
    GeoDataFrame containing the basic_polygon polygon.
    """
    poly_a = Polygon([(7, 9), (7, 11.25), (9.25, 11.25), (9.25, 9), (7, 9)])
    poly_b = Polygon(
        [(12, 14), (12, 16.25), (14.25, 16.25), (14.25, 14), (12, 14)]
    )
    gdf = gpd.GeoDataFrame(
        [1, 2], geometry=[poly_a, basic_polygon], crs="epsg:4326",
    )
    multi_gdf = gpd.GeoDataFrame(
        [1, 2], geometry=[gdf.unary_union, poly_b], crs="epsg:4326",
    )
    multi_gdf["attr"] = ["attr1", "attr2"]
    return multi_gdf


@pytest.fixture
def poly_geo_plot(basic_polygon_gdf):
    """Create a polygon vector tester object."""
    _, ax = plt.subplots()

    basic_polygon_gdf.plot(ax=ax)

    return VectorTester(ax)


@pytest.fixture
def multi_poly_geo_plot(multi_polygon_gdf):
    """Create a mutlipolygon vector tester object."""
    _, ax = plt.subplots()

    multi_polygon_gdf.plot(ax=ax)

    return VectorTester(ax)


@pytest.fixture
def multi_poly_geo_plot_attributes(multi_polygon_gdf):
    """Create a mutlipolygon vector tester object grouped by attributes."""
    _, ax = plt.subplots()

    multi_polygon_gdf.plot(ax=ax, column="attr")

    return VectorTester(ax)


def test_list_of_polygons_check(poly_geo_plot, basic_polygon):
    """Check that the polygon assert works with a list of polygons."""
    x, y = basic_polygon.exterior.coords.xy
    poly_list = [list(zip(x, y))]
    poly_geo_plot.assert_polygons(poly_list)
    plt.close("all")


def test_polygon_geodataframe_check(poly_geo_plot, basic_polygon_gdf):
    """Check that the polygon assert works with a polygon geodataframe"""
    poly_geo_plot.assert_polygons(basic_polygon_gdf)
    plt.close("all")


def test_empty_list_polygon_check(poly_geo_plot):
    """Check that the polygon assert fails an empty list."""
    with pytest.raises(ValueError, match="Empty list or GeoDataFrame "):
        poly_geo_plot.assert_polygons([])
        plt.close("all")


def test_empty_list_entry_polygon_check(poly_geo_plot):
    """Check that the polygon assert fails a list with an empty entry."""
    with pytest.raises(ValueError, match="Empty list or GeoDataFrame "):
        poly_geo_plot.assert_polygons([[]])
        plt.close("all")


def test_empty_gdf_polygon_check(poly_geo_plot):
    """Check that the polygon assert fails an empty GeoDataFrame."""
    with pytest.raises(ValueError, match="Empty list or GeoDataFrame "):
        poly_geo_plot.assert_polygons(gpd.GeoDataFrame([]))
        plt.close("all")


def test_polygon_dec_check(poly_geo_plot, basic_polygon):
    """
    Check that the polygon assert passes when the polygon is off by less than
    the maximum decimal precision.
    """
    x, y = basic_polygon.exterior.coords.xy
    poly_list = [[(x[0] + 0.1, x[1]) for x in list(zip(x, y))]]
    poly_geo_plot.assert_polygons(poly_list, dec=1)
    plt.close("all")


def test_polygon_dec_check_fail(poly_geo_plot, basic_polygon):
    """
    Check that the polygon assert fails when the polygon is off by more than
    the maximum decimal precision.
    """
    with pytest.raises(AssertionError, match="Incorrect Polygon"):
        x, y = basic_polygon.exterior.coords.xy
        poly_list = [(x[0] + 0.5, x[1]) for x in list(zip(x, y))]
        poly_geo_plot.assert_polygons(poly_list, dec=1)
        plt.close("all")


def test_polygon_custom_fail_message(poly_geo_plot, basic_polygon):
    """Check that the corrct error message is raised when polygons fail"""
    with pytest.raises(AssertionError, match="Test Message"):
        x, y = basic_polygon.exterior.coords.xy
        poly_list = [(x[0] + 0.5, x[1]) for x in list(zip(x, y))]
        poly_geo_plot.assert_polygons(poly_list, m="Test Message")
        plt.close("all")


def test_multi_polygon_pass(multi_poly_geo_plot, multi_polygon_gdf):
    """Check a multipolygon passes"""
    multi_poly_geo_plot.assert_polygons(multi_polygon_gdf)
    plt.close("all")


def test_assert_polygons_grouped_pass(
    multi_poly_geo_plot_attributes, multi_polygon_gdf
):
    """Check that assert_polys_grouped_by_type passes"""
    multi_poly_geo_plot_attributes.assert_polys_grouped_by_type(
        multi_polygon_gdf, "attr"
    )
    plt.close("all")


def test_assert_polygons_grouped_fail(multi_poly_geo_plot, multi_polygon_gdf):
    """Check that assert_polys_grouped_by_type fails bad gdf"""
    with pytest.raises(
        AssertionError, match="Polygon attributes not accurate"
    ):
        multi_poly_geo_plot.assert_polys_grouped_by_type(
            multi_polygon_gdf, "attr"
        )
        plt.close("all")


def test_assert_polygons_grouped_passes_nonetype(
    multi_poly_geo_plot_attributes,
):
    """Check that assert_polys_grouped_by_type passes when polys_expected is
    None"""
    multi_poly_geo_plot_attributes.assert_polys_grouped_by_type(None, None)
    plt.close("all")


def test_assert_polygons_grouped_fails_list(multi_poly_geo_plot_attributes):
    """Check that assert_polys_grouped_by_type fails when polys_expected is not
    a gdf"""
    with pytest.raises(ValueError, match="polys_expected is not of expected "):
        multi_poly_geo_plot_attributes.assert_polys_grouped_by_type(
            [1, 2, 3], "attr"
        )
        plt.close("all")


def test_assert_polygons_grouped_passes_custom_message(
    multi_poly_geo_plot, multi_polygon_gdf
):
    """Test that a custom fail message is raised if given"""
    with pytest.raises(AssertionError, match="Test message"):
        multi_poly_geo_plot.assert_polys_grouped_by_type(
            multi_polygon_gdf, "attr", m="Test message"
        )
        plt.close("all")


def test_get_polygons_by_attributes_correct(multi_poly_geo_plot_attributes):
    """Test that get_polys_by_attributes returns correctly"""
    polys_list = [
        [
            [(2.0, 2.0), (2.0, 4.25), (4.25, 4.25), (4.25, 2.0), (2.0, 2.0)],
            [(7.0, 9.0), (7.0, 11.25), (9.25, 11.25), (9.25, 9.0), (7.0, 9.0)],
        ],
        [
            [
                (12.0, 14.0),
                (12.0, 16.25),
                (14.25, 16.25),
                (14.25, 14.0),
                (12.0, 14.0),
            ]
        ],
    ]
    assert (
        polys_list == multi_poly_geo_plot_attributes.get_polys_by_attributes()
    )
    plt.close("all")
