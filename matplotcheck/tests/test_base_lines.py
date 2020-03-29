import pytest
from matplotcheck.base import PlotTester
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

"""Fixtures"""


@pytest.fixture
def pd_df_reg_data():
    data = {
        "A": [1.2, 1.9, 3.0, 4.1, 4.6, 6.0, 6.9, 8.4, 9.0],
        "B": [2.4, 3.9, 6.1, 7.8, 9.0, 11.5, 15.0, 16.2, 18.6],
    }

    return pd.DataFrame(data)


@pytest.fixture
def pt_reg_data(pd_df_reg_data):
    fig, ax = plt.subplots()
    sns.regplot("A", "B", data=pd_df_reg_data, ax=ax)

    return PlotTester(ax)


@pytest.fixture
def pt_one2one():
    fig, ax = plt.subplots()
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls="--", c="k")

    return PlotTester(ax)


@pytest.fixture
def pt_reg_one2one(pd_df_reg_data):
    fig, ax = plt.subplots()
    sns.regplot("A", "B", data=pd_df_reg_data, ax=ax)
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls="--", c="k")

    return PlotTester(ax)


def test_reg_plot(pd_df_reg_data, pt_reg_data):

    # Get the correct slope and intercept for the data
    slope_exp, intercept_exp, _, _, _ = stats.linregress(
        pd_df_reg_data.A, pd_df_reg_data.B
    )

    pt_reg_data.assert_line(slope_exp, intercept_exp)


def test_reg_plot_slope_fails(pd_df_reg_data, pt_reg_data):
    _, intercept_exp, _, _, _ = stats.linregress(
        pd_df_reg_data.A, pd_df_reg_data.B
    )
    with pytest.raises(AssertionError, match="Expected line not displayed"):
        pt_reg_data.assert_line(1, intercept_exp)


def test_reg_plot_intercept_fails(pd_df_reg_data, pt_reg_data):

    slope_exp, _, _, _, _ = stats.linregress(
        pd_df_reg_data.A, pd_df_reg_data.B
    )

    with pytest.raises(AssertionError, match="Expected line not displayed"):
        pt_reg_data.assert_line(slope_exp, 1)


def test_line_type_reg(pt_reg_data):
    pt_reg_data.assert_lines_of_type("regression")


def test_line_type_one2one(pt_one2one):
    pt_one2one.assert_lines_of_type("onetoone")


def test_line_type_reg_one2one(pt_reg_one2one):
    pt_reg_one2one.assert_lines_of_type(["regression", "onetoone"])


def test_line_type_reg_fails(pt_one2one):
    with pytest.raises(
        AssertionError, match="regression line not displayed properly"
    ):
        pt_one2one.assert_lines_of_type("regression")


def test_line_type_one2one_fails(pt_reg_data):
    with pytest.raises(
        AssertionError, match="onetoone line not displayed properly"
    ):
        pt_reg_data.assert_lines_of_type("onetoone")
