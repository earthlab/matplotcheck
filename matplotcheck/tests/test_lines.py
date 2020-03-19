"""Tests for the vector module"""
import pytest
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import LineString
from matplotcheck.vector import VectorTester
import matplotlib

matplotlib.use("Agg")


@pytest.fixture
def multi_line_gdf(two_line_gdf):
    """ Create a multi-line GeoDataFrame.
    This has one multi line and another regular line.
    """
    # Create a single and multi line object
    multiline_feat = two_line_gdf.unary_union
    linec = LineString([(2, 1), (3, 1), (4, 1), (5, 2)])
    out_df = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries([multiline_feat, linec]), crs="epsg:4326",
    )
    out_df["attr"] = ["road", "stream"]
    return out_df


@pytest.fixture
def mixed_type_geo_plot(pd_gdf, multi_line_gdf):
    """Create a point plot for testing"""
    _, ax = plt.subplots()

    pd_gdf.plot(ax=ax)
    multi_line_gdf.plot(ax=ax)

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def poly_line_plot(two_line_gdf):
    """Create a line vector tester object."""
    _, ax = plt.subplots()

    two_line_gdf.plot(ax=ax)

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def poly_multiline_plot(multi_line_gdf):
    """Create a multiline vector tester object."""
    _, ax = plt.subplots()

    multi_line_gdf.plot(ax=ax, column="attr")

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def poly_multiline_plot_bad(multi_line_gdf):
    """Create a multiline vector tester object."""
    _, ax = plt.subplots()

    multi_line_gdf.plot(ax=ax)

    axis = plt.gca()

    return VectorTester(axis)


def test_assert_line_geo(poly_line_plot, two_line_gdf):
    """Test that lines are asserted correctly"""
    poly_line_plot.assert_lines(two_line_gdf)
    plt.close("all")


def test_assert_multiline_geo(poly_multiline_plot, multi_line_gdf):
    """Test that multi lines are asserted correctly"""
    poly_multiline_plot.assert_lines(multi_line_gdf)
    plt.close("all")


def test_assert_line_geo_fail(poly_line_plot, multi_line_gdf):
    """Test that lines fail correctly"""
    with pytest.raises(AssertionError, match="Incorrect Line Data"):
        poly_line_plot.assert_lines(multi_line_gdf)
        plt.close("all")


def test_assert_multiline_geo_fail(poly_multiline_plot, two_line_gdf):
    """Test that multi lines fail correctly"""
    with pytest.raises(AssertionError, match="Incorrect Line Data"):
        poly_multiline_plot.assert_lines(two_line_gdf)
        plt.close("all")


def test_assert_line_fails_list(poly_line_plot):
    """Test that assert_lines fails when passed a list"""
    linelist = [
        [(1, 1), (2, 2), (3, 2), (5, 3)],
        [(3, 4), (5, 7), (12, 2), (10, 5), (9, 7.5)],
    ]
    with pytest.raises(ValueError, match="lines_expected is not expected ty"):
        poly_line_plot.assert_lines(linelist)
        plt.close("all")


def test_assert_line_geo_passed_nothing(poly_line_plot):
    """Test that assertion passes when passed None"""
    poly_line_plot.assert_lines(None)
    plt.close("all")


def test_get_lines_geometry(poly_line_plot):
    """Test that get_lines returns the proper values"""
    lines = [(LineString(i[0])) for i in poly_line_plot.get_lines().values]
    geometries = gpd.GeoDataFrame(geometry=lines)
    poly_line_plot.assert_lines(geometries)
    plt.close("all")


def test_assert_lines_grouped_by_type(poly_multiline_plot, multi_line_gdf):
    """Test that assert works for grouped line plots"""
    poly_multiline_plot.assert_lines_grouped_by_type(multi_line_gdf, "attr")
    plt.close("all")


def test_assert_lines_grouped_by_type_fail(
    poly_multiline_plot_bad, multi_line_gdf
):
    """Test that assert fails for incorrectly grouped line plots"""
    with pytest.raises(AssertionError, match="Line attributes not accurate "):
        poly_multiline_plot_bad.assert_lines_grouped_by_type(
            multi_line_gdf, "attr"
        )
        plt.close("all")


def test_assert_lines_grouped_by_type_passes_with_none(poly_multiline_plot):
    """Test that assert passes if nothing is passed into it"""
    poly_multiline_plot.assert_lines_grouped_by_type(None, None)
    plt.close("all")


def test_assert_lines_grouped_by_type_fails_non_gdf(
    poly_multiline_plot, multi_line_gdf
):
    """Test that assert fails if a list is passed into it"""
    with pytest.raises(ValueError, match="lines_expected is not of expected "):
        poly_multiline_plot.assert_lines_grouped_by_type(
            multi_line_gdf.to_numpy(), "attr"
        )
        plt.close("all")


def test_mixed_type_passes(mixed_type_geo_plot, pd_gdf):
    """Tests that points passes with a mixed type plot"""
    mixed_type_geo_plot.assert_points(pd_gdf)
    plt.close("all")


def test_get_lines_by_collection(poly_multiline_plot):
    """Test that get_lines_by_collection returns the correct values"""
    lines_list = [
        [
            [(1, 1), (2, 2), (3, 2), (5, 3)],
            [(3, 4), (5, 7), (12, 2), (10, 5), (9, 7.5)],
            [(2, 1), (3, 1), (4, 1), (5, 2)],
        ]
    ]
    sorted_lines_list = sorted([sorted(l) for l in lines_list])
    assert sorted_lines_list == poly_multiline_plot.get_lines_by_collection()
    plt.close("all")
