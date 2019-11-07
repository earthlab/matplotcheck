"""Tests for the base module -- titles and captions"""
import pytest
import matplotlib.pyplot as plt


""" TITLE TESTS """


def test_correct_title(pt_line_plt):
    """Check that the correct plot title is grabbed from the axis object.
    Note that get_titles maintains case."""

    assert "Plot Title" in pt_line_plt.get_titles()[1]
    plt.close()


def test_get_titles(pt_line_plt):
    """Check that the correct plot title is grabbed from the axis object.
    Note that get_titles maintains case."""
    assert "My Plot Title" == pt_line_plt.get_titles()[1]
    plt.close()


def test_get_titles_suptitle(pt_line_plt):
    """Check that the correct suptitle gets grabbed from a figure with 2 subplots"""
    assert "My Figure Title" == pt_line_plt.get_titles()[0]
    plt.close()


def test_title_contains_empty_expect(pt_line_plt):
    """Check title_contains when expected title is empty"""
    pt_line_plt.assert_title_contains([])
    plt.close()


def test_title_contains_expect_none(pt_line_plt):
    """Check title_contains when expected title is None"""
    pt_line_plt.assert_title_contains(None)
    plt.close()


def test_title_contains_axes(pt_line_plt):
    """Check title_contains for axes title"""
    pt_line_plt.assert_title_contains(
        ["My", "Plot", "Title"], title_type="axes"
    )
    plt.close()


def test_title_contains_axes_badtext(pt_line_plt):
    """Check title_contains fails when given bad text"""
    with pytest.raises(
        AssertionError, match="Title does not contain expected string: foo"
    ):
        pt_line_plt.assert_title_contains(
            ["Title", "foo", "bar"], title_type="axes"
        )
    plt.close()


def test_title_contains_invalid_title_type(pt_line_plt):
    """Check title_contains raises value error when given invalid title type"""
    with pytest.raises(
        ValueError, match="title_type must be one of the following"
    ):
        pt_line_plt.assert_title_contains(["Title"], title_type="all")
    plt.close()


def test_title_contains_figure(pt_line_plt):
    """Check title_contains tester for figure/sup title"""
    pt_line_plt.assert_title_contains(
        ["My", "Figure", "Title"], title_type="figure"
    )
    plt.close()


def test_title_contains_figure_nosuptitle(pt_bar_plt):
    """Check title_contains tester for figure title fails when there is no suptitle"""
    with pytest.raises(
        AssertionError, match="Expected title is not displayed"
    ):
        pt_bar_plt.assert_title_contains(
            ["My", "Figure", "Title"], title_type="figure"
        )
    plt.close()


def test_title_contains_both_axes_figure(pt_line_plt):
    """Check title_contains tester for combined axes + figure titles"""
    pt_line_plt.assert_title_contains(
        ["My", "Figure", "Plot", "Title"], title_type="either"
    )
    plt.close()


def test_title_contains_both_axes_figure_badtext(pt_line_plt):
    """Check title_contains tester for combined titles, should fail with bad text"""
    with pytest.raises(
        AssertionError, match="Title does not contain expected string: foo"
    ):
        pt_line_plt.assert_title_contains(
            ["My", "Figure", "Plot", "Title", "foo"], title_type="either"
        )
    plt.close()


""" CAPTION TESTS """


def test_get_caption(pt_line_plt):
    """Make sure that get caption returns correct text string"""
    assert "Figure Caption" == pt_line_plt.get_caption()
    plt.close()


def test_assert_caption_contains(pt_line_plt):
    """Test that caption contains passes given right text"""
    pt_line_plt.assert_caption_contains([["Figure"], ["Caption"]])
    plt.close()


def test_assert_caption_contains_expect_empty(pt_line_plt):
    """Test that caption contains passes when expected text list is empty"""
    pt_line_plt.assert_caption_contains([])
    plt.close()


def test_assert_caption_contains_expect_none(pt_line_plt):
    """Test that caption contains passes when expected text is None"""
    pt_line_plt.assert_caption_contains(None)
    plt.close()


def test_assert_caption_contains_badtext(pt_line_plt):
    """Test that caption contains passes given wrong text"""
    with pytest.raises(
        AssertionError, match="Caption does not contain expected string: foo"
    ):
        pt_line_plt.assert_caption_contains([["foo"], ["bar"]])
    plt.close()


def test_assert_caption_contains_nocaption(pt_bar_plt):
    """Test that caption_contains fails when there is no caption"""
    with pytest.raises(
        AssertionError, match="No caption exists in appropriate location"
    ):
        pt_bar_plt.assert_caption_contains([["Figure"], ["Caption"]])
    plt.close()
