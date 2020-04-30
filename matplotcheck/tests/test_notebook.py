"""Tests for the notebook module"""

import pytest
import matplotlib.pyplot as plt
from matplotcheck.base import PlotTester
import matplotcheck.notebook as nb


@pytest.fixture
def locals_dictionary_good():
    """Abriged locals dictionary of a jupyter notebook with import in the proper
    place"""
    return {
        "__name__": "__main__",
        "__doc__": "Automatically created module for IPython interactive",
        "_ih": ["", "import os", 'print("Good notebook")', "locals()"],
        "In": ["", "import os", 'print("Good notebook")', "locals()"],
        "Out": {},
        "_i": 'print("Good notebook")',
        "_ii": "import os",
        "_iii": "",
        "_i1": "import os",
        "_i2": 'print("Good notebook")',
        "_i3": "locals()",
    }


@pytest.fixture
def locals_dictionary_bad():
    """Abriged locals dictionary of a jupyter notebook with import in the wrong
    place"""
    return {
        "__name__": "__main__",
        "__doc__": "Automatically created module for IPython interactive",
        "_ih": ["", 'print("Bad notebook")', "import os", "locals()"],
        "In": ["", 'print("Bad notebook")', "import os", "locals()"],
        "Out": {},
        "_i": "import os",
        "_ii": 'print("Bad notebook")',
        "_iii": "",
        "_i1": 'print("Bad notebook")',
        "_i2": "import os",
        "_i3": "locals()",
    }


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


def test_error_test_count_pass(capsys):
    """Test error test prints out correct statement when passing"""
    nb.error_test(1, 1)
    captured = capsys.readouterr()
    assert captured.out == "ERRORS TEST: PASSED!\n"


def test_error_test_count(capsys):
    """Test error test prints out correct statement when failing"""
    nb.error_test(1, 2)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "ERRORS TEST: FAILED! 1 of 2 Cells ran without errors\n"
    )


def test_remove_comments_with_comments():
    """Test remove comments returns string without comments"""
    test_string = """Hello\n# comments\ntest\nstring"""
    commentless = nb.remove_comments(test_string)
    assert commentless == """Hello\ntest\nstring"""


def test_remove_comments_without_comments():
    """Test remove comments leaves commentless string alone"""
    test_string = """Hello\ntest\nstring"""
    commentless = nb.remove_comments(test_string)
    assert commentless == """Hello\ntest\nstring"""


def test_import_test_pass(capsys, locals_dictionary_good):
    """Test import test passes when import are done correctly"""
    nb.import_test(locals_dictionary_good, 3)
    captured = capsys.readouterr()
    assert captured.out == "IMPORT TEST: PASSED!\n"


def test_import_test_fail(capsys, locals_dictionary_bad):
    """Test import test passes when import are done incorrectly"""
    nb.import_test(locals_dictionary_bad, 3)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "IMPORT TEST: FAILED! Import statement found in cell 2\n"
    )
