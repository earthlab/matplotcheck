"""Pytest fixtures for matplotcheck tests"""
import pytest
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotcheck.base import PlotTester


@pytest.fixture
def pd_df():
    """Create a pandas dataframe for testing"""
    return pd.DataFrame(
        {"A": np.arange(100), "B": np.random.randint(0, 100, size=100)}
    )


@pytest.fixture
def pd_df_timeseries():
    """Create a pandas dataframe for testing, with timeseries in one column"""
    return pd.DataFrame(
        {
            "time": pd.date_range(start="1/1/2018", periods=100),
            "A": np.random.randint(0, 100, size=100),
        }
    )


@pytest.fixture
def pd_gdf():
    """Create a geopandas GeoDataFrame for testing"""
    df = pd.DataFrame(
        {
            "lat": np.random.randint(-85, 85, size=100),
            "lon": np.random.randint(-180, 180, size=100),
        }
    )
    gdf = gpd.GeoDataFrame(
        {"A": np.arange(100)}, geometry=gpd.points_from_xy(df.lon, df.lat)
    )

    return gdf


@pytest.fixture
def pd_xlabels():
    """Create a DataFrame which uses the column labels as x-data."""
    df = pd.DataFrame({"B": bp.random.randint(0, 100, size=100)})


@pytest.fixture
def pt_scatter_plt(pd_df):
    """Create scatter plot for testing"""
    fig, ax = plt.subplots()

    pd_df.plot("A", "B", kind="scatter", ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def pt_line_plt(pd_df):
    """Create line plot for testing"""
    fig, ax = plt.subplots()

    # Basic plot plus title, x and y axis labels
    pd_df.plot("A", "B", kind="line", ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    plt.suptitle("My Figure Title")
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")
    ax.set_xlim((0, 100))
    ax.set_ylim((0, 100))

    # Insert caption
    ax_position = ax.get_position()
    fig.text(
        ax_position.ymax - 0.25, ax_position.ymin - 0.075, "Figure Caption"
    )

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def pt_multi_line_plt(pd_df):
    """Line plot with multiple data columns, plus legend"""
    fig, ax = plt.subplots()
    pd_df.plot(ax=ax)
    ax.set_ylim((0, 140))
    ax.legend(loc="center left", title="Legend", bbox_to_anchor=(1, 0.5))

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def pt_bar_plt(pd_df):
    """Create bar plot for testing"""
    fig, ax = plt.subplots()

    pd_df.plot("A", "B", kind="bar", ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def pt_time_line_plt(pd_df_timeseries):
    """Create timeseries line plot for testing"""
    fig, ax = plt.subplots()

    pd_df_timeseries.plot("time", "A", kind="line", ax=ax)

    axis = plt.gca()

    return PlotTester(axis)


@pytest.fixture
def pt_geo_plot(pd_gdf):
    """Create a geo plot for testing"""
    fig, ax = plt.subplots()

    pd_gdf.plot(ax=ax)
    ax.set_title("My Plot Title", fontsize=30)
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")

    axis = plt.gca()

    return PlotTester(axis)
