"""Tests for the raster module"""
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
from matplotcheck.base import PlotTester
from matplotcheck.raster import RasterTester


@pytest.fixture
def np_ar():
    """Create numpy array for image plot testing"""
    return np.random.rand(100, 100)


@pytest.fixture
def np_ar_discrete():
    """Numpy array with discrete values for image plot testing"""
    return np.random.choice(4, (10, 10))


@pytest.fixture
def pd_raster_plt(np_ar):
    """Create raster plot for testing"""
    fig, ax = plt.subplots()
    im = ax.imshow(np_ar)
    ax.set_title("My Plot Title", fontsize=30)
    fig.colorbar(im)

    axis = plt.gca()
    return RasterTester(axis)


@pytest.fixture
def pd_raster_class_plt(np_ar_discrete):
    """Class/discrete raster plot for testing"""
    values = np.sort(np.unique(np_ar_discrete))

    fig, ax = plt.subplots()
    im = ax.imshow(
        np_ar_discrete, interpolation="none", cmap=plt.get_cmap("tab10")
    )
    ax.set_title("My Plot Title", fontsize=30)
    colors = [im.cmap(im.norm(val)) for val in values]
    patches = [
        mpatches.Patch(color=colors[i], label="Level {l}".format(l=values[i]))
        for i in range(values.shape[0])
    ]
    plt.legend(handles=patches)

    axis = plt.gca()
    return RasterTester(axis)


def test_raster_assert_image(pd_raster_plt, np_ar):
    """Check that RasterTester image checker works"""

    # Check that assert_image works
    pd_raster_plt.assert_image(np_ar)

    # Check to make sure this fails
    bad_ar = np_ar + 1
    with pytest.raises(AssertionError):
        pd_raster_plt.assert_image(bad_ar)


def test_raster_assert_image_fullscreen(pd_raster_plt):
    """Checks that image takes up full screen"""
    pd_raster_plt.assert_image_full_screen()


def test_get_colorbars(pd_raster_plt):
    """Check that get_colorbars correctly retrieves the correct object"""

    cb = pd_raster_plt.get_colorbars()
    assert len(cb) == 1
    assert isinstance(cb[0], matplotlib.colorbar.Colorbar)


def test_raster_assert_colorbar_range(pd_raster_plt, np_ar):
    """Colorbar range checker, should be set to min and max of input array"""

    pd_raster_plt.assert_colorbar_range([np_ar.min(), np_ar.max()])

    with pytest.raises(AssertionError):
        pd_raster_plt.assert_colorbar_range([-1, np_ar.max()])
        pd_raster_plt.assert_colorbar_range([np_ar.min(), np_ar.max() + 0.1])


def test_raster_assert_legend_accuracy_classified_image(
    pd_raster_class_plt, np_ar_discrete
):
    """Colorbar range checker, should be set to min and max of input array"""

    values = np.sort(np.unique(np_ar_discrete))
    label_options = [[str(i)] for i in values]

    pd_raster_class_plt.assert_legend_accuracy_classified_image(
        np_ar_discrete, label_options
    )

    # Test that it fails with bad label or image
    bad_label_options = [["foo"] * values.shape[0]]
    bad_image = np_ar_discrete + 1

    with pytest.raises(AssertionError):
        pd_raster_class_plt.assert_legend_accuracy_classified_image(
            np_ar_discrete, bad_label_options
        )
        pd_raster_class_plt.assert_legend_accuracy_classified_image(
            bad_image, label_options
        )
