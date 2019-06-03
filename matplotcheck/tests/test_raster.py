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
        np_ar_discrete, interpolation="none", cmap=plt.get_cmap("tab10")
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


def test_raster_get_colorbars_length(raster_plt):
    """Check that get_colorbars correctly retrieves 1 colorbar from raster_plt1"""
    # Should only be 1 object, and should be a colorbar object
    cb = raster_plt.get_colorbars()
    assert len(cb) == 1
    plt.close()




def test_raster_get_colorbars_type(raster_plt):
    """Check that get_colorbars retrieves a colorbar object"""
    cb = raster_plt.get_colorbars()
    assert isinstance(cb[0], matplotlib.colorbar.Colorbar)
    plt.close()


def test_raster_assert_colorbar_range(raster_plt, np_ar):
    """Colorbar range checker, should be set to min and max of input array"""
    # Colorbar range should be min and max
    raster_plt.assert_colorbar_range([np_ar.min(), np_ar.max()])
    plt.close()


def test_raster_assert_colorbar_range_wrongmin(raster_plt, np_ar):
    """Colorbar range checker should fail with the wrong max"""
    # Should fail with min value
    with pytest.raises(
        AssertionError,
        match="Colorbar minimum is not expected value:{}".format(
            np_ar.min() - 1
        ),
    ):
        raster_plt.assert_colorbar_range([np_ar.min() - 1, np_ar.max()])
    plt.close()


def test_raster_assert_colorbar_range_wrongmax(raster_plt, np_ar):
    """Colorbar range checker should fail with the wrong min"""
    # Should fail with wrong max value
    with pytest.raises(
        AssertionError,
        match="Colorbar maximum is not expected value:{}".format(
            np_ar.max() + 0.1
        ),
    ):
        raster_plt.assert_colorbar_range([np_ar.min(), np_ar.max() + 0.1])
    plt.close()


def test_raster_assert_colorbar_range_multiple(raster_plt, np_ar):
    """Colorbar range checker should fail when there are multiple colorbars"""
    # Add a second colorbar
    raster_plt.ax.imshow(np_ar)
    raster_plt.ax.get_figure().colorbar(raster_plt.ax.images[1], raster_plt.ax)
    with pytest.raises(
        AssertionError, match="Exactly one colorbar should be displayed"
    ):
        raster_plt.assert_colorbar_range([np_ar.min(), np_ar.max()])
    plt.close()


def test_raster_assert_colorbar_range_blank(raster_plt_blank, np_ar):
    """Colorbar range checker should fail if no image has been added to axes"""
    # Should fail with no image on axis
    with pytest.raises(AssertionError, match="No image found on axes"):
        raster_plt_blank.assert_colorbar_range([np_ar.min(), np_ar.max()])
    plt.close()


""" LEGEND TESTS """


def test_raster_assert_legend_accuracy(raster_plt_class, np_ar_discrete):
    """Checks that legend matches image, checking both the labels and color patches"""
    values = np.sort(np.unique(np_ar_discrete))
    label_options = [[str(i)] for i in values]

    raster_plt_class.assert_legend_accuracy_classified_image(
        np_ar_discrete, label_options
    )
    plt.close()


def test_raster_assert_legend_accuracy_badlabel(
    raster_plt_class, np_ar_discrete
):
    """Checks that legend matches image, should fail with bad labels"""
    values = np.sort(np.unique(np_ar_discrete))

    # Should fail with bad label
    bad_label_options = [["foo"] * values.shape[0]]
    with pytest.raises(AssertionError, match="Incorrect legend labels"):
        raster_plt_class.assert_legend_accuracy_classified_image(
            np_ar_discrete, bad_label_options
        )
    plt.close()


def test_raster_assert_legend_accuracy_badvalues(
    raster_plt_class, np_ar_discrete
):
    """Checks that legend matches image, should fail if you swap image values"""
    values = np.sort(np.unique(np_ar_discrete))
    label_options = [[str(i)] for i in values]

    # Swap image values without updating plot colors
    bad_image = np_ar_discrete
    bad_image[bad_image == 0] = 1

    # Should fail with bad image
    with pytest.raises(
        AssertionError, match="Incorrect legend to data relation"
    ):
        raster_plt_class.assert_legend_accuracy_classified_image(
            bad_image, label_options
        )
    plt.close()


def test_raster_assert_legend_accuracy_nolegend(raster_plt, np_ar_discrete):
    """Check that assert_legend_accuracy fails if there is no legend"""
    values = np.sort(np.unique(np_ar_discrete))
    label_options = [[str(i)] for i in values]

    # Fails without legend
    with pytest.raises(AssertionError, match="No legend displayed"):
        raster_plt.assert_legend_accuracy_classified_image(
            np_ar_discrete, label_options
        )
    plt.close()


def test_raster_assert_legend_accuracy_noimage(
    raster_plt_blank, np_ar_discrete
):
    """Check that assert_legend_accuracy fails if there is no image"""
    values = np.sort(np.unique(np_ar_discrete))
    label_options = [[str(i)] for i in values]

    # Fails when no image displayed
    with pytest.raises(AssertionError, match="No Image Displayed"):
        raster_plt_blank.assert_legend_accuracy_classified_image(
            np_ar_discrete, label_options
        )
    plt.close()


""" IMAGE TESTS """


def test_raster_assert_image(raster_plt, np_ar):
    """Checks that assert_image passes only when plot data matches array"""
    raster_plt.assert_image(np_ar)
    plt.close()


def test_raster_assert_image_baddata(raster_plt, np_ar):
    """assert_image should fail when we change the array values"""
    # Should fail with wrong array
    bad_ar = np_ar + 1
    with pytest.raises(AssertionError, match="Arrays are not equal"):
        raster_plt.assert_image(bad_ar)
    plt.close()


def test_raster_assert_image_blank(raster_plt_blank, np_ar):
    """"assert_image should fail with blank image"""
    with pytest.raises(AssertionError, match="No Image Displayed"):
        raster_plt_blank.assert_image(np_ar)
    plt.close()


def test_raster_assert_image_rgb(raster_plt_rgb, np_ar_rgb):
    """Check assert_image for a 3-band RGB image"""
    raster_plt_rgb.assert_image(np_ar_rgb)
    plt.close()


def test_raster_assert_image_rgb_baddata(raster_plt_rgb, np_ar_rgb):
    """Check assert_image fails with bad data for rgb plot"""
    bad_ar = np_ar_rgb + 1
    with pytest.raises(AssertionError, match="Arrays are not equal"):
        raster_plt_rgb.assert_image(bad_ar)
    plt.close()


def test_raster_assert_image_class(raster_plt_class, np_ar_discrete):
    """Check assert_image for a discrete, classified image"""
    raster_plt_class.assert_image(np_ar_discrete, im_classified=True)
    plt.close()


def test_raster_assert_image_class_baddata(raster_plt_class, np_ar_discrete):
    """Check that assert_image with bad data fails for a discrete, classified image"""
    bad_ar = np_ar_discrete + 1
    with pytest.raises(AssertionError, match="Arrays are not equal"):
        raster_plt_class.assert_image(bad_ar)
    plt.close()


def test_raster_assert_image_fullscreen(raster_plt):
    """Checks that the first image on axis takes up full axis"""
    raster_plt.assert_image_full_screen()
    plt.close()


def test_raster_assert_image_fullscreen_fail_xlims(raster_plt):
    """assert fullscreen should fail if we modify the x-axis limits"""
    cur_xlim, cur_ylim = raster_plt.ax.get_xlim(), raster_plt.ax.get_ylim()
    raster_plt.ax.set_xlim([cur_xlim[0], cur_xlim[1] + 5])
    with pytest.raises(
        AssertionError, match="Image is stretched inaccurately"
    ):
        raster_plt.assert_image_full_screen()
    plt.close()


def test_raster_assert_image_fullscreen_fail_ylims(raster_plt):
    """assert fullscreen should fail if we modify the x-axis limits"""
    cur_xlim, cur_ylim = raster_plt.ax.get_xlim(), raster_plt.ax.get_ylim()
    raster_plt.ax.set_xlim([cur_xlim[0], cur_xlim[1]])
    raster_plt.ax.set_ylim([cur_ylim[0], cur_ylim[1] - 1])
    with pytest.raises(
        AssertionError, match="Image is stretched inaccurately"
    ):
        raster_plt.assert_image_full_screen()
    plt.close()


def test_raster_assert_image_fullscreen_blank(raster_plt_blank):
    """assert_image_fullscreen should fail with blank image"""
    with pytest.raises(AssertionError, match="No image found on axes"):
        raster_plt_blank.assert_image_full_screen()
    plt.close()
