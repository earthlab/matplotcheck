"""Tests for the notebook module"""

import pytest
import matplotlib
import matplotlib.pyplot as plt
import matplotcheck.notebook as nb


def test_notebook_convert_single_axes(basic_polygon_gdf):
    """Test convert single axes."""
    fig, ax = plt.subplots()
    basic_polygon_gdf.plot(ax=ax)
    assert (
        str(type(nb.convert_axes(plt)))
        == "<class 'matplotlib.axes._subplots.AxesSubplot'>"
    )
