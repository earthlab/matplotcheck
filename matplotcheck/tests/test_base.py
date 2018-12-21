"""Tests for the base module"""
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotcheck.base import PlotTester

@pytest.fixture
def pd_df():
    """Create a pandas dataframe for testing"""
    return pd.DataFrame(np.random.randint(0,100,size=(100, 2)), columns=list('AB'))

@pytest.fixture
def pd_df_plt():
    """Create a pandas dataframe for testing"""
    # Can a fixture take data from another fixture??
    pd_df = pd.DataFrame(np.random.randint(0, 100, size=(100, 2)), columns=list('AB'))
    fig, ax = plt.subplots()
    pd_df.plot('A', 'B',
               kind='scatter',
               ax=ax)

    ax.set_title("My Plot Title",
                 fontsize=30)

    axis = plt.gca()
    return PlotTester(axis)


def test_something(pd_df_plt):
    """Test to ensure that the correct plot title is grabbed from the axis object.
    Note that get_titles maintains case"""

    assert "Plot Title" in pd_df_plt.get_titles()[1]



def test_plot():
    pass