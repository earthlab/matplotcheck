"""Tests for the raster module"""
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotcheck.base import PlotTester
from matplotcheck.raster import RasterTester


@pytest.fixture
def np_ar():
    """Create numpy array for image plot testing"""
    return np.random.rand(100, 100)


@pytest.fixture
def pd_raster_plt(np_ar):
    """Create raster plot for testing"""
    fig, ax = plt.subplots()
    ax.imshow(np_ar)
    ax.set_title("My Plot Title", fontsize=30)

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
    pd_raster_plt.assert_image_full_screen()
