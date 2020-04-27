import pytest
from matplotcheck.base import PlotTester
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

"""Fixtures"""


@pytest.fixture
def pd_df_reg_data():
    """Create a pandas dataframe with points that are roughly along the same
    line."""
    data = {
        "A": [1.2, 1.9, 3.0, 4.1, 4.6, 6.0, 6.9, 8.4, 9.0],
        "B": [2.4, 3.9, 6.1, 7.8, 9.0, 11.5, 15.0, 16.2, 18.6],
    }

    return pd.DataFrame(data)


@pytest.fixture
def pt_reg_data(pd_df_reg_data):
    """Create a PlotTester object with a regression line"""
    fig, ax = plt.subplots()
    sns.regplot("A", "B", data=pd_df_reg_data, ax=ax)

    return PlotTester(ax)


@pytest.fixture
def pt_one2one():
    """Create a PlotTester object a one-to-one line"""
    fig, ax = plt.subplots()
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls="--", c="k")

    return PlotTester(ax)


@pytest.fixture
def pt_reg_one2one(pd_df_reg_data):
    """Create a PlotTester object with a regression line and a one-to-one
    line"""
    fig, ax = plt.subplots()
    sns.regplot("A", "B", data=pd_df_reg_data, ax=ax)
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls="--", c="k")

    return PlotTester(ax)


def test_reg_plot(pd_df_reg_data, pt_reg_data):
    """Test that assert_line() correctly passes when given the correct slope
    and intercept."""
    # Get the correct slope and intercept for the data
    slope_exp, intercept_exp, _, _, _ = stats.linregress(
        pd_df_reg_data.A, pd_df_reg_data.B
    )

    pt_reg_data.assert_line(slope_exp, intercept_exp)


def test_reg_plot_slope_fails(pd_df_reg_data, pt_reg_data):
    """Check that assert_line() correctly falis when given an incorrect
    slope."""
    _, intercept_exp, _, _, _ = stats.linregress(
        pd_df_reg_data.A, pd_df_reg_data.B
    )
    with pytest.raises(AssertionError, match="Expected line not displayed"):
        pt_reg_data.assert_line(1, intercept_exp)


def test_reg_plot_intercept_fails(pd_df_reg_data, pt_reg_data):
    """Check that assert_line() correctly fails when given an incorrect
    intercept"""
    slope_exp, _, _, _, _ = stats.linregress(
        pd_df_reg_data.A, pd_df_reg_data.B
    )

    with pytest.raises(AssertionError, match="Expected line not displayed"):
        pt_reg_data.assert_line(slope_exp, 1)


def test_line_type_reg(pt_reg_data):
    """Check that assert_lines_of_type() correctly passes when checking for a
    regression line."""
    pt_reg_data.assert_lines_of_type("regression")


def test_line_type_one2one(pt_one2one):
    """Check that assert_lines_of_type() correctly passes when checking for a
    one-to-one line."""
    pt_one2one.assert_lines_of_type("onetoone")


def test_line_type_reg_one2one(pt_reg_one2one):
    """Check that assert_lines_of_type() correctly passes when checking for
    both a regression line and a one-to-one line."""
    pt_reg_one2one.assert_lines_of_type(["regression", "onetoone"])


def test_line_type_reg_fails(pt_one2one):
    """Check that assert_lines_of_type() correctly fails when checking for a
    regression line, but one does not exist."""
    with pytest.raises(
        AssertionError, match="regression line not displayed properly"
    ):
        pt_one2one.assert_lines_of_type("regression")


def test_line_type_one2one_fails(pt_reg_data):
    """Check that assert_lines_of_type() correctly fails when checking for a
    one-to-one line, but one does not exist."""
    with pytest.raises(
        AssertionError, match="onetoone line not displayed properly"
    ):
        pt_reg_data.assert_lines_of_type("onetoone")
