"""Tests for the base module -- legends"""
import pytest
import matplotlib.pyplot as plt


""" LEGEND TESTS """


def test_assert_legend_titles(pt_multi_line_plt):
    """Test for checking that legend tites are equal to given string"""
    pt_multi_line_plt.assert_legend_titles(["legend"])


def test_assert_legend_titles_not_case_sensitive(pt_multi_line_plt):
    """Check that assert_legend_titles is NOT case sensitive"""
    pt_multi_line_plt.assert_legend_titles(["LeGenD"])


def test_assert_legend_titles_bad_text(pt_multi_line_plt):
    """Check that assert_legend_titles fails with wrong text"""
    with pytest.raises(
        AssertionError,
        match="Legend title does not contain expected string: foo",
    ):
        pt_multi_line_plt.assert_legend_titles(["foo"])


def test_assert_legend_titles_wrong_num(pt_multi_line_plt):
    """Check assert_legend_titles fails when expected # of titles != # of legends"""
    with pytest.raises(
        AssertionError, match="Incorrect number of legend exist"
    ):
        pt_multi_line_plt.assert_legend_titles(["legend", "legend2"])


def test_assert_legend_labels(pt_multi_line_plt):
    """Test for checking that legend labels are expected strings"""
    pt_multi_line_plt.assert_legend_labels(["a", "b"])


def test_assert_legend_not_case_sensitive(pt_multi_line_plt):
    """Check that assert_legend_labels is NOT case sensitive"""
    pt_multi_line_plt.assert_legend_labels(["A", "B"])


def test_assert_legend_labels_bad_text(pt_multi_line_plt):
    """Check that assert_legend_labels raises expected error when given wrong text"""
    with pytest.raises(
        AssertionError, match="Legend does not have expected labels"
    ):
        pt_multi_line_plt.assert_legend_labels(["a", "c"])


def test_assert_legend_labels_wrong_num(pt_multi_line_plt):
    """Check that assert_legend_labels raises expected error given wrong number of labels"""
    with pytest.raises(
        AssertionError,
        match="Legend does not contain expected number of entries",
    ):
        pt_multi_line_plt.assert_legend_labels(["a", "b", "c"])


def test_assert_legend_no_overlay_content(pt_multi_line_plt):
    """Test for checking whether legend overlays plot contents"""
    pt_multi_line_plt.assert_legend_no_overlay_content()


def test_assert_legend_no_overlay_content_fail(pt_multi_line_plt):
    """assert_legend_no_overlay should fail when legend is in center of plot"""
    pt_multi_line_plt.ax.legend(loc="center")
    with pytest.raises(AssertionError, match="Legend overlays plot window"):
        pt_multi_line_plt.assert_legend_no_overlay_content()


def test_assert_no_legend_overlap_single(pt_multi_line_plt):
    """Checks that assert_no_legend_overlap passes when only one legend"""
    pt_multi_line_plt.assert_no_legend_overlap()


def test_assert_no_legend_overlap_double(pt_multi_line_plt):
    """Checks that assert_no_legend_overlap passes when two legends don't overlap"""
    leg_1 = plt.legend(loc=[0.8, 0.8])
    leg_2 = plt.legend(loc=[0.1, 0.1])
    pt_multi_line_plt.ax.add_artist(leg_1)
    pt_multi_line_plt.assert_no_legend_overlap()


def test_assert_no_legend_overlap_fail(pt_multi_line_plt):
    """Checks that assert_no_legend_overlap fails with overlapping legends"""
    leg_1 = plt.legend(loc=[0.12, 0.12])
    leg_2 = plt.legend(loc=[0.1, 0.1])
    pt_multi_line_plt.ax.add_artist(leg_1)
    with pytest.raises(AssertionError, match="Legends overlap eachother"):
        pt_multi_line_plt.assert_no_legend_overlap()