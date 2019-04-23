"""Tests for the raster module"""
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
from matplotcheck.raster import RasterTester


@pytest.fixture
def np_ar():
    """Create numpy array for image plot testing"""
    return np.random.rand(100, 100)


@pytest.fixture
def np_ar_rgb():
    """Create rgb numpy array for image plot testing"""
    return np.random.randint(0, 255, size=(100, 100, 3))


@pytest.fixture
def np_ar_discrete():
    """Create numpy array with discrete values for image plot testing"""
    return np.random.choice(4, (10, 10))


@pytest.fixture
def raster_plt(np_ar):
    """Create simple raster plot for testing"""
    fig, ax = plt.subplots()
    im = ax.imshow(np_ar)
    ax.set_title("My Plot Title", fontsize=30)
    fig.colorbar(im)

    axis = plt.gca()
    return RasterTester(axis)


@pytest.fixture
def raster_plt_rgb(np_ar_rgb):
    """Create 3-band raster RGB plot for testing"""
    fig, ax = plt.subplots()
    ax.imshow(np_ar_rgb)

    axis = plt.gca()
    return RasterTester(axis)


@pytest.fixture
def raster_plt_blank():
    """Blank axis for testing. No image is plotted"""
    fig, ax = plt.subplots()

    axis = plt.gca()
    return RasterTester(axis)


@pytest.fixture
def raster_plt_class(np_ar_discrete):
    """Classified/discrete raster plot for testing"""
    values = np.sort(np.unique(np_ar_discrete))

    fig, ax = plt.subplots()
    im = ax.imshow(
        np_ar_discrete, interpolation='none', cmap=plt.get_cmap('tab10')
    )
    ax.set_title("My Plot Title", fontsize=30)

    # Create legend
    colors = [im.cmap(im.norm(val)) for val in values]
    patches = [
        mpatches.Patch(color=colors[i], label="Level {l}".format(l=values[i]))
        for i in range(values.shape[0])
    ]
    plt.legend(handles=patches)

    axis = plt.gca()
    return RasterTester(axis)


""" COLORBAR TESTS """


def test_raster_get_colorbars(raster_plt):
    """Check that get_colorbars correctly retrieves the correct object type"""

    cb = raster_plt.get_colorbars()
    assert len(cb) == 1
    assert isinstance(cb[0], matplotlib.colorbar.Colorbar)


def test_raster_assert_colorbar_range(raster_plt, np_ar):
    """Colorbar range checker, should be set to min and max of input array"""
    raster_plt.assert_colorbar_range([np_ar.min(), np_ar.max()])

    # Should fail with wrong min and max values
    with pytest.raises(
        AssertionError,
        match="Colorbar minimum is not expected value:{}".format(np_ar.min() - 1)
    ):
        raster_plt.assert_colorbar_range([np_ar.min() - 1, np_ar.max()])
    with pytest.raises(
        AssertionError,
        match="Colorbar maximum is not expected value:{}".format(np_ar.max() + 0.1)
    ):
        raster_plt.assert_colorbar_range([np_ar.min(), np_ar.max() + 0.1])

    # Add a second colorbar, should fail
    raster_plt.ax.imshow(np_ar)
    raster_plt.ax.get_figure().colorbar(raster_plt.ax.images[1], raster_plt.ax)
    with pytest.raises(
        AssertionError,
        match="Exactly one colorbar should be displayed"
    ):
        raster_plt.assert_colorbar_range([np_ar.min(), np_ar.max()])


""" LEGEND TESTS """


def test_raster_assert_legend_accuracy_classified_image(
    raster_plt_class, raster_plt_blank, raster_plt, np_ar_discrete
):
    """Checks that legend matches image, checking both the labels and color patches"""
    values = np.sort(np.unique(np_ar_discrete))
    label_options = [[str(i)] for i in values]

    raster_plt_class.assert_legend_accuracy_classified_image(
        np_ar_discrete, label_options
    )

    # Fails without legend
    with pytest.raises(AssertionError, match="No legend displayed"):
        raster_plt.assert_legend_accuracy_classified_image(
            np_ar_discrete, label_options
        )

    # Fails when no image displayed
    with pytest.raises(AssertionError, match="No Image Displayed"):
        raster_plt_blank.assert_legend_accuracy_classified_image(
            np_ar_discrete,
            label_options)

    # Should fail with bad label
    bad_label_options = [["foo"] * values.shape[0]]
    with pytest.raises(AssertionError, match="Incorrect legend labels"):
        raster_plt_class.assert_legend_accuracy_classified_image(
            np_ar_discrete, bad_label_options
        )

    # Should fail if you swap image values without updating plot colors
    bad_image = np_ar_discrete
    bad_image[bad_image==0] = 1
    with pytest.raises(AssertionError, match="Incorrect legend to data relation"):
        raster_plt_class.assert_legend_accuracy_classified_image(
            bad_image, label_options
        )


""" IMAGE TESTS """


def test_raster_assert_image(raster_plt, np_ar):
    """Checks that assert_image passes only when plot data matches array"""

    # Check that assert_image works
    raster_plt.assert_image(np_ar)

    # Should fail with wrong array
    bad_ar = np_ar + 1
    with pytest.raises(AssertionError, match="Arrays are not equal"):
        raster_plt.assert_image(bad_ar)


def test_raster_assert_image_rgb(raster_plt_rgb, np_ar_rgb):
    raster_plt_rgb.assert_image(np_ar_rgb)


def test_raster_assert_image_class(raster_plt_class, np_ar_discrete):
    raster_plt_class.assert_image(np_ar_discrete, im_classified=True)


def test_raster_assert_image_fullscreen(raster_plt, raster_plt_blank):
    """Checks that image takes up full screen"""
    raster_plt.assert_image_full_screen()
    with pytest.raises(AssertionError):
        raster_plt_blank.assert_image_full_screen()
