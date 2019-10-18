"""Tests for the base module -- axis"""
import pytest
import matplotlib.pyplot as plt


""" AXIS TESTS """


def test_axis_off_fail_on(pt_line_plt):
    """Check assert_axis_off fails when axis lines are on"""
    # Should fail when axis are on (by default)
    with pytest.raises(
        AssertionError, match="Axis lines are displayed on plot"
    ):
        pt_line_plt.assert_axis_off()
    plt.close()


def test_axis_off_turned_off(pt_line_plt):
    """Check assert_axis_off for case when axis are turned off"""
    # Turn off axis and test again
    pt_line_plt.ax.axis("off")
    pt_line_plt.assert_axis_off()
    plt.close()


def test_axis_off_vis_false(pt_line_plt):
    """Check assert_axis_off for case when axis visibility set to False"""
    pt_line_plt.ax.xaxis.set_visible(False)
    pt_line_plt.ax.yaxis.set_visible(False)
    pt_line_plt.assert_axis_off()
    plt.close()


def test_axis_off_one_visible(pt_line_plt):
    """Check assert_axis_off fails when x or y axis is set to visible"""
    # Should fail with either axis visible
    pt_line_plt.ax.xaxis.set_visible(True)
    pt_line_plt.ax.yaxis.set_visible(False)
    with pytest.raises(
        AssertionError, match="Axis lines are displayed on plot"
    ):
        pt_line_plt.assert_axis_off()

    pt_line_plt.ax.xaxis.set_visible(False)
    pt_line_plt.ax.yaxis.set_visible(True)
    with pytest.raises(
        AssertionError, match="Axis lines are displayed on plot"
    ):
        pt_line_plt.assert_axis_off()
    plt.close()


def test_axis_off_empty_ticks(pt_line_plt):
    """Check assert_axis_off for case when axis tick labels set to empty lists"""
    pt_line_plt.ax.xaxis.set_ticks([])
    pt_line_plt.ax.yaxis.set_ticks([])
    pt_line_plt.assert_axis_off()
    plt.close()


def test_axis_off_non_empty_ticks(pt_line_plt):
    """Check assert_axis_off fails when axis tick list is not empty"""
    # Should fail with either axis ticks turned on
    pt_line_plt.ax.xaxis.set_ticks([1])
    pt_line_plt.ax.yaxis.set_ticks([])
    with pytest.raises(
        AssertionError, match="Axis lines are displayed on plot"
    ):
        pt_line_plt.assert_axis_off()

    pt_line_plt.ax.xaxis.set_ticks([])
    pt_line_plt.ax.yaxis.set_ticks([1])
    with pytest.raises(
        AssertionError, match="Axis lines are displayed on plot"
    ):
        pt_line_plt.assert_axis_off()
    plt.close()


def test_axis_label_contains_x(pt_line_plt):
    """Checks for assert_axis_label_contains for x axis"""
    pt_line_plt.assert_axis_label_contains(
        axis="x", strings_expected=["x", "label"]
    )
    plt.close()


def test_axis_label_contains_y(pt_line_plt):
    """Checks for assert_axis_label_contains for y axis"""
    pt_line_plt.assert_axis_label_contains(axis="y", strings_expected=["y"])
    plt.close()


def test_axis_label_contains_invalid_axis(pt_line_plt):
    """Check that assert_axis_label_contains fails when given unexpected axis"""
    # Fails when given an invalid axies
    with pytest.raises(ValueError, match="axis must be one of the following"):
        pt_line_plt.assert_axis_label_contains(
            axis="z", strings_expected=["y"]
        )
    plt.close()


def test_axis_label_contains_bad_text(pt_line_plt):
    """Check that assert_axis_label_contains fails with text not in label"""
    with pytest.raises(
        AssertionError,
        match="x-axis label does not contain expected string: foo",
    ):
        pt_line_plt.assert_axis_label_contains(
            axis="x", strings_expected=["x", "foo"]
        )
    plt.close()


def test_axis_label_contains_expect_none(pt_multi_line_plt):
    """Check assert_axis_label_contains passes when expected text is blank"""
    pt_multi_line_plt.assert_axis_label_contains(
        axis="x", strings_expected=None
    )
    plt.close()


def test_axis_label_contains_no_label(pt_multi_line_plt):
    """Check assert_axis_label_contains fails when there is no axis label"""
    with pytest.raises(
        AssertionError, match="Expected x axis label is not displayed"
    ):
        pt_multi_line_plt.assert_axis_label_contains(
            axis="x", strings_expected=["foo"]
        )

    with pytest.raises(
        AssertionError, match="Expected y axis label is not displayed"
    ):
        pt_multi_line_plt.assert_axis_label_contains(
            axis="y", strings_expected=["foo"]
        )
    plt.close()


def test_assert_lims_x_pass(pt_line_plt):
    """Test for axis limit assertion x axis (exact values)"""
    pt_line_plt.assert_lims([0, 100], axis="x")
    plt.close()


def test_assert_lims_y_pass(pt_line_plt):
    """Test for axis limit assertion y axis (exact values)"""
    pt_line_plt.assert_lims([0, 100], axis="y")
    plt.close()


def test_assert_lims_y_bad_lims(pt_line_plt):
    """Test that assert_lims fails with bad values for y axis"""
    # Bad max
    with pytest.raises(AssertionError, match="Incorrect limits on the y axis"):
        pt_line_plt.assert_lims([0, 101], axis="y")
    # Bad min
    with pytest.raises(AssertionError, match="Incorrect limits on the y axis"):
        pt_line_plt.assert_lims([1, 100], axis="y")
    plt.close()


def test_assert_lims_x_bad_lims(pt_line_plt):
    """Test that assert_lims fails with bad values for x axis"""
    # Bad max
    with pytest.raises(AssertionError, match="Incorrect limits on the x axis"):
        pt_line_plt.assert_lims([0, 101], axis="x")
    # Bad min
    with pytest.raises(AssertionError, match="Incorrect limits on the x axis"):
        pt_line_plt.assert_lims([1, 100], axis="x")
    plt.close()


def test_assert_lims_invalid_axis(pt_line_plt):
    """Test that assert_lims fails with invalid axis (z)"""
    with pytest.raises(
        ValueError, match="axis must be one of the following string"
    ):
        pt_line_plt.assert_lims([0, 100], axis="z")
    plt.close()


def test_assert_lims_range_x_pass(pt_line_plt):
    """Test that x axis limit assertion range passes as expected"""
    pt_line_plt.assert_lims_range(((-5, 5), (95, 105)), axis="x")
    pt_line_plt.assert_lims_range(((0, 0), (100, 100)), axis="x")
    plt.close()


def test_assert_lims_range_y_pass(pt_line_plt):
    """Test that y axis limit assertion range passes as expected"""
    pt_line_plt.assert_lims_range(((-5, 5), (95, 105)), axis="y")
    pt_line_plt.assert_lims_range(((0, 0), (100, 100)), axis="y")
    plt.close()


def test_assert_lims_range_y_bad_lims(pt_line_plt):
    """Test that assert_lims_range fails with bad values for y axis"""
    with pytest.raises(
        AssertionError, match="Incorrect max limit on the y axis"
    ):
        pt_line_plt.assert_lims_range(((-5, 5), (95, 99)), axis="y")
    with pytest.raises(
        AssertionError, match="Incorrect min limit on the y axis"
    ):
        pt_line_plt.assert_lims_range(((1, 5), (95, 105)), axis="y")
    plt.close()


def test_assert_lims_range_x_bad_lims(pt_line_plt):
    """Test that assert_lims_range fails with bad values for x axis"""
    with pytest.raises(
        AssertionError, match="Incorrect max limit on the x axis"
    ):
        pt_line_plt.assert_lims_range(((-5, 5), (95, 98)), axis="x")
    with pytest.raises(
        AssertionError, match="Incorrect min limit on the x axis"
    ):
        pt_line_plt.assert_lims_range(((1, 5), (95, 105)), axis="x")
    plt.close()


def test_assert_lims_range_invalid_axis(pt_line_plt):
    """Test that assert_lims_range fails with invalid axis (z)"""
    with pytest.raises(
        ValueError, match="axis must be one of the following string"
    ):
        pt_line_plt.assert_lims_range(((-5, 5), (95, 105)), axis="z")
    plt.close()


def test_assert_equal_xlims_ylims(pt_line_plt):
    """Checks that axis xlims and ylims are equal, as expected"""
    pt_line_plt.assert_equal_xlims_ylims()
    plt.close()


def test_assert_equal_xlims_ylims_bad_xlims(pt_line_plt):
    """Checks that assert_equal_xlims_ylims fails when we change x axis lims"""
    # Check y axis
    pt_line_plt.ax.set_xlim((0, 99))
    with pytest.raises(AssertionError, match="xlims and ylims are not equal"):
        pt_line_plt.assert_equal_xlims_ylims()
    plt.close()


def test_assert_equal_xlims_ylims_bad_ylims(pt_line_plt):
    """Checks that assert_equal_xlims_ylims fails when we change y axis lims"""
    # Check y axis
    pt_line_plt.ax.set_ylim((1, 100))
    with pytest.raises(AssertionError, match="xlims and ylims are not equal"):
        pt_line_plt.assert_equal_xlims_ylims()
    plt.close()
