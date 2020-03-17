"""Tests for the vector module"""
import pytest
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import LineString
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
    _, ax = plt.subplots()

    pd_gdf.plot(ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def bad_pd_gdf(pd_gdf):
    """Create a point geodataframe with slightly wrong values for testing"""
    return gpd.GeoDataFrame(
        geometry=gpd.points_from_xy(
            pd_gdf.geometry.x + 1, pd_gdf.geometry.y + 1
        )
    )


@pytest.fixture
def two_line_gdf():
    """ Create Line Objects For Testing """
    linea = LineString([(1, 1), (2, 2), (3, 2), (5, 3)])
    lineb = LineString([(3, 4), (5, 7), (12, 2), (10, 5), (9, 7.5)])
    gdf = gpd.GeoDataFrame([1, 2], geometry=[linea, lineb], crs="epsg:4326")
    return gdf


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
def poly_line_plot(two_line_gdf):
    """Create a line vector tester object."""
    _, ax = plt.subplots()

    two_line_gdf.plot(ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def poly_multiline_plot(multi_line_gdf):
    """Create a multiline vector tester object."""
    _, ax = plt.subplots()

    multi_line_gdf.plot(ax=ax, column="attr")
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def pt_geo_plot(pd_gdf):
    """Create a geo plot for testing"""
    fig, ax = plt.subplots()
    size = 0
    point_symb = {"Tree": "green", "Bush": "brown"}

    for ctype, points in pd_gdf.groupby("attr"):
        color = point_symb[ctype]
        label = ctype
        size += 100
        points.plot(color=color, ax=ax, label=label, markersize=size)

    ax.legend(title="Legend", loc=(1.1, 0.1))

    axis = plt.gca()

    return VectorTester(axis)


@pytest.fixture
def pt_geo_plot_bad(pd_gdf):
    """Create a geo plot for testing"""
    fig, ax = plt.subplots()
    pd_gdf.plot(ax=ax, column="attr")
    axis = plt.gca()

    return VectorTester(axis)


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
    assert list(sorted(xy_values.x)) == sorted(list(pd_gdf.geometry.x))
    assert list(sorted(xy_values.y)) == sorted(list(pd_gdf.geometry.y))


def test_assert_points_custom_message(point_geo_plot, bad_pd_gdf):
    """Tests that a custom error message is passed."""
    message = "Test message"
    with pytest.raises(AssertionError, match="Test message"):
        point_geo_plot.assert_points(points_expected=bad_pd_gdf, m=message)


def test_assert_line_geo(poly_line_plot, two_line_gdf):
    """Test that lines are asserted correctly"""
    poly_line_plot.assert_lines(two_line_gdf)
    plt.close()


def test_assert_multiline_geo(poly_multiline_plot, multi_line_gdf):
    """Test that multi lines are asserted correctly"""
    poly_multiline_plot.assert_lines(multi_line_gdf)
    plt.close()


def test_assert_line_geo_fail(poly_line_plot, multi_line_gdf):
    """Test that lines fail correctly"""
    with pytest.raises(AssertionError, match="Incorrect Line Data"):
        poly_line_plot.assert_lines(multi_line_gdf)
        plt.close()


def test_assert_multiline_geo_fail(poly_multiline_plot, two_line_gdf):
    """Test that multi lines fail correctly"""
    with pytest.raises(AssertionError, match="Incorrect Line Data"):
        poly_multiline_plot.assert_lines(two_line_gdf)
        plt.close()


def test_assert_line_fails_list(poly_line_plot):
    """Test that assert_lines fails when passed a list"""
    linelist = [
        [(1, 1), (2, 2), (3, 2), (5, 3)],
        [(3, 4), (5, 7), (12, 2), (10, 5), (9, 7.5)],
    ]
    with pytest.raises(ValueError, match="lines_expected is not expected ty"):
        poly_line_plot.assert_lines(linelist)
        plt.close()


def test_assert_line_geo_passed_nothing(poly_line_plot):
    """Test that assertion passes when passed None"""
    poly_line_plot.assert_lines(None)
    plt.close()


def test_get_lines_geometry(poly_line_plot):
    """Test that get_lines returns the proper values"""
    lines = [(LineString(i[0])) for i in poly_line_plot.get_lines().values]
    geometries = gpd.GeoDataFrame(geometry=lines)
    poly_line_plot.assert_lines(geometries)
    plt.close()


# def test_legend_no_overlay_pass(pt_geo_plot):
#     """Test that no_overlay passes when the legend doesn't overlay"""
#     pt_geo_plot.assert_legend_no_overlay_content()


# Broken right now, not sure why
# def test_legend_no_overlay_pass(pt_geo_plot):
#     """Test that no_overlay passes when the legend doesn't overlay"""
#     pt_geo_plot.assert_legend_no_overlay_content()


# Broken right now, not sure why
# def test_legend_no_overlay_fail(pt_geo_plot_bad_legend):
#     """Test that no_overlay fails when the legends do overlay"""
#     with pytest.raises(AssertionError, match="Legend overlays plot contents"):
#         pt_geo_plot_bad_legend.assert_legend_no_overlay_content()


# Broken right now, not sure why
# def test_legends_no_overlap_pass(pt_geo_plot):
#     """Test that legends pass if they don't overlay"""
#     pt_geo_plot.assert_no_legend_overlap()


# Broken right now, not sure why
# def test_legend_no_overlap_fail(pt_geo_plot_bad_legend):
#     """Test that legends fail if they overlap"""
#     with pytest.raises(AssertionError, match="Legends overlap eachother"):
#         pt_geo_plot_bad_legend.assert_no_legend_overlap()


# Broken right now, not sure why
# def test_assert_lines_grouped_by_type(poly_multiline_plot, multi_line_gdf):
#     """Test that assert works for grouped line plots"""
#     poly_multiline_plot.assert_lines_grouped_by_type(multi_line_gdf, "attr")


def test_points_sorted_by_markersize_pass(pt_geo_plot, pd_gdf):
    """Test points sorted by size of attribute pass"""
    pt_geo_plot.assert_collection_sorted_by_markersize(pd_gdf, "attr")


def test_points_sorted_by_markersize_fail(pt_geo_plot_bad, pd_gdf):
    """Test points sorted by size of attribute"""
    with pytest.raises(AssertionError, match="Markersize not based on"):
        pt_geo_plot_bad.assert_collection_sorted_by_markersize(pd_gdf, "attr")
