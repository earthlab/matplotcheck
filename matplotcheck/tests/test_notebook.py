"""Tests for the notebook module"""

import pytest
import matplotlib
import matplotlib.pyplot as plt
from matplotcheck.base import PlotTester
import matplotcheck.notebook as nb


@pytest.fixture
def locals_dictionary_good():
    """Abriged locals dictionary of a jupyter notebook with import in the proper
    place. The locals dictionary can be found by running the locals()
    function in a jupyter notebook. It gives information about the notebook
    contents that we can check to ensure imports are done at the beginning
    of the notebook."""
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
    place. The locals dictionary can be found by running the locals()
    function in a jupyter notebook. It gives information about the notebook
    contents that we can check to ensure imports are done at the beginning
    of the notebook."""
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
    """Test converting a single axes plot."""
    fig, ax = plt.subplots()
    basic_polygon_gdf.plot(ax=ax)
    ax.set_title("Title")
    store = nb.convert_axes(plt)

    assert isinstance(store, matplotlib.pyplot.Axes)
    PlotTester(store).assert_title_contains([["Title"]])

    plt.close()


def test_notebook_convert_multi_axes(basic_polygon_gdf):
    """Test convert multi axes returns a list of all axes available."""
    titles = ["Title1", "Title2"]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    basic_polygon_gdf.plot(ax=ax1)
    basic_polygon_gdf.plot(ax=ax2)
    ax1.set_title(titles[0])
    ax2.set_title(titles[1])
    store = nb.convert_axes(plt, which_axes="all")

    assert isinstance(store, list)
    assert len(store) == 2

    for i, axes in enumerate(store):
        PlotTester(axes).assert_title_contains(titles[i])
    plt.close()


def test_notebook_convert_last_axes(basic_polygon_gdf):
    """Test convert last axes returns the last axes plotted by matplotlib."""
    titles = ["Title1", "Title2"]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    basic_polygon_gdf.plot(ax=ax1)
    basic_polygon_gdf.plot(ax=ax2)
    ax1.set_title(titles[0])
    ax2.set_title(titles[1])
    store = nb.convert_axes(plt, which_axes="last")

    assert isinstance(store, matplotlib.pyplot.Axes)
    PlotTester(store).assert_title_contains(titles[1])

    plt.close()


def test_notebook_convert_first_axes(basic_polygon_gdf):
    """Test convert first axes returns the first axes plotted by matplotlib."""
    titles = ["Title1", "Title2"]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    basic_polygon_gdf.plot(ax=ax1)
    basic_polygon_gdf.plot(ax=ax2)
    ax1.set_title(titles[0])
    ax2.set_title(titles[1])
    store = nb.convert_axes(plt, which_axes="first")

    assert isinstance(store, matplotlib.pyplot.Axes)
    PlotTester(store).assert_title_contains(titles[0])

    plt.close()


def test_notebook_convert_last_empty_axes(basic_polygon_gdf):
    """Test convert last with an empty axes to ensure it returns the correct
    axes even when one is empty."""

    fig, (ax1, ax2) = plt.subplots(1, 2)
    basic_polygon_gdf.plot(ax=ax1)
    ax1.set_title("Title1")
    store = nb.convert_axes(plt, which_axes="last")

    assert isinstance(store, matplotlib.pyplot.Axes)
    with pytest.raises(
        AssertionError, match="Expected title is not displayed"
    ):
        PlotTester(store).assert_title_contains("Title1")

    plt.close()


def test_notebook_convert_all_empty_axes(basic_polygon_gdf):
    """Test convert all with an empty axes to ensure it returns the correct
    axes in a list even when one is empty."""

    fig, (ax1, ax2) = plt.subplots(1, 2)
    basic_polygon_gdf.plot(ax=ax1)
    ax1.set_title("Title1")
    store = nb.convert_axes(plt, which_axes="all")

    assert isinstance(store, list)
    assert len(store) == 2

    PlotTester(store[0]).assert_title_contains("Title1")
    with pytest.raises(
        AssertionError, match="Expected title is not displayed"
    ):
        PlotTester(store[1]).assert_title_contains("Title1")

    plt.close()


def test_notebook_convert_axes_error(basic_polygon_gdf):
    """Test convert_axes() throws an error when given a bad string."""
    fig, ax = plt.subplots()
    basic_polygon_gdf.plot(ax=ax)
    with pytest.raises(ValueError, match="which_axes must be one of the "):
        nb.convert_axes(plt, which_axes="error")
    plt.close()


def test_error_test_count_pass(capsys):
    """Test error_test() prints out correct statement when passing."""
    nb.error_test(1, 1)
    captured = capsys.readouterr()
    assert captured.out == "ERRORS TEST: PASSED!\n"


def test_error_test_count(capsys):
    """Test error_test() prints out correct statement when failing."""
    nb.error_test(1, 2)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "ERRORS TEST: FAILED! 1 of 2 Cells ran without errors\n"
    )


def test_remove_comments_with_comments():
    """Test remove_comments() returns string without comments."""
    test_string = """Hello\n# comments\ntest\nstring"""
    commentless = nb.remove_comments(test_string)
    assert commentless == """Hello\ntest\nstring"""


def test_remove_comments_without_comments():
    """Test remove_comments() leaves commentless string alone."""
    test_string = """Hello\ntest\nstring"""
    commentless = nb.remove_comments(test_string)
    assert commentless == """Hello\ntest\nstring"""


def test_import_test_pass(capsys, locals_dictionary_good):
    """Test import_test() passes when imports are done correctly."""
    nb.import_test(locals_dictionary_good, 3)
    captured = capsys.readouterr()
    assert captured.out == "IMPORT TEST: PASSED!\n"


def test_import_test_fail(capsys, locals_dictionary_bad):
    """Test import_test() fails when imports are done incorrectly."""
    nb.import_test(locals_dictionary_bad, 3)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "IMPORT TEST: FAILED! Import statement found in cell 2\n"
    )


def test_import_test_pass_when_not_checking(capsys, locals_dictionary_bad):
    """Test import_test() passes when imports are done incorrectly but not
    checked."""
    nb.import_test(locals_dictionary_bad, 1)
    captured = capsys.readouterr()
    assert captured.out == "IMPORT TEST: PASSED!\n"
