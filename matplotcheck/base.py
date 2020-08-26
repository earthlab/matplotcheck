"""
matplotcheck.base
=================

Base plot checking class and methods that should apply to all plots
whether they are spatial or not.

"""

import numpy as np
import matplotlib
from matplotlib.backend_bases import RendererBase
import math
from scipy import stats
import pandas as pd
import numbers
import geopandas as gpd


class InvalidPlotError(Exception):
    pass


class PlotTester(object):
    """
    Object to grab elements from Matplotlib plots
    Temporarily removing parameters and returns as it's breaking sphinx

    Parameters
    ----------
    axis : mpl axis object

    """

    def __init__(self, ax):
        """Initialize TestPlot object"""
        self.ax = ax

    def _is_line(self):
        """Boolean expressing if ax contains scatter points.
        If plot contains scatter points and lines return True.

        Returns
        -------
        is_line : boolean
            True if Axes ax is a line plot, False if not
        """

        if self.ax.lines:
            for line in self.ax.lines:
                if (
                    not line.get_linestyle()
                    or not line.get_linewidth()
                    or line.get_linewidth() > 0
                ):
                    return True

    def _is_scatter(self):
        """Boolean expressing if ax contains scatter points.
        If plot contains scatter points as well as lines, functions will return
        true.

        Returns
        -------
        is_scatter : boolean
            True if Axes ax is a scatter plot, False if not
        """
        if self.ax.collections:
            return True
        elif self.ax.lines:
            for line in self.ax.lines:
                if (
                    line.get_linestyle() == "None"
                    or line.get_linewidth() == "None"
                    or line.get_linewidth() == 0
                ):
                    return True
        return False

    def assert_string_contains(
        self,
        string,
        strings_expected,
        message_default="String does not contain expected string: {0}",
        message_or="String does not contain at least one of: {0}",
    ):
        """Asserts that `string` contains the expected strings from
        `strings_expected`.

        Parameters
        ----------
        strings_expected : list
            Any string in `strings_expected` must be in the title for the
            assertion to pass. If there is a list of strings in
            `strings_expected`, at least one of the strings in that list must
            be in the title for the assertion to pass. For example, if
            ``strings_expected=['a', 'b', 'c']``, then ``'a'`` AND ``'b'`` AND
            ``'c'`` must be in the title for the assertion to pass.
            Alternatively, if ``strings_expected=['a', 'b', ['c', 'd']]``, then
            ``'a'`` AND ``'b'`` AND (at least one of: ``'c'``, ``'d'``) must be
            in the title for the assertion to pass. Case insensitive.
        message_default : string
            The error message to be displayed if the `string` does not contain
            a string in strings_expected. If `message` contains ``'{0}'``, it
            will be replaced with the first expected string not found in the
            label.
        message_or : string
            Similar to `message_default`, `message_or` is the error message to
            be displated if `string` does not contain at least one of
            the strings in an inner list in `strings_expected`. If `message`
            contains ``'{0}'``, it will be replaced with the first failing
            inner list in `strings_expected`.

        Raises
        -------
        AssertionError
            if `string` does not contain expected strings
        """
        # Assertion passes if strings_expected == [] or
        # strings_expected == None
        if not strings_expected:
            return

        string = string.lower().replace(" ", "")

        if isinstance(strings_expected, str):
            strings_expected = [strings_expected]

        for check in strings_expected:
            if isinstance(check, str):
                if not check.lower().replace(" ", "") in string:
                    raise AssertionError(message_default.format(check))
            elif isinstance(check, list):
                if not any(
                    [c.lower().replace(" ", "") in string for c in check]
                ):
                    if len(check) == 1:
                        raise AssertionError(message_default.format(check[0]))
                    else:
                        raise AssertionError(message_or.format(check))
            else:
                raise ValueError(
                    "str_lst must be a list of: lists or strings."
                )

    def assert_plot_type(
        self, plot_type=None, message="Plot is not of type {0}"
    ):
        """Asserts Axes `ax` contains the type of plot specified in `plot_type`.
        if `plot_type` is ``None``, assertion is passed.

        Parameters
        ----------
        plot_type: string
            String specifying the expected plot type. Options:
            `scatter`, `bar`, `line`
        message : string
            The error message to be displayed if Plot does not match
            `plot_type`. If `message` contains ``'{0}'``, it will be replaced
            with the epected plot type.

        Raises
        -------
        AssertionError
            if Plot does not match `plot_type`
        """
        if plot_type:
            if plot_type == "scatter":
                assert self._is_scatter(), message.format(plot_type)
            elif plot_type == "bar":
                assert self.ax.patches, message.format(plot_type)
            elif plot_type == "line":
                assert self._is_line(), message.format(plot_type)
            else:
                raise ValueError(
                    "Plot_type to test must be either: scatter, bar or line"
                )

    """ TITLES TESTS/HELPER FUNCTIONS """

    def get_titles(self):
        """Returns the suptitle (Figure title) and axes title of `ax`.

        Returns
        -------
        suptitle : string
            Figure title of the Figure that the `ax` object is on. If figure
            title is ``None``, this is an empty string.
        title : string
            Title on the axes. If title is ``None``, this is an empty string.
        """
        fig, suptitle = self.ax.get_figure(), ""
        if fig._suptitle:
            suptitle += fig._suptitle.get_text()
        return suptitle, self.ax.get_title()

    def assert_title_contains(
        self,
        strings_expected,
        title_type="either",
        message_default="Title does not contain expected string: {0}",
        message_or="Title does not contain at least one of: {0}",
        message_no_title="Expected title is not displayed",
    ):
        """Asserts that title defined by `title_type` contains the expected
        strings from `strings_expected`.

        Parameters
        ----------
        strings_expected : list
            Any string in `strings_expected` must be in the title for the
            assertion to pass. If there is a list of strings in
            `strings_expected`, at least one of the strings in that list must
            be in the title for the assertion to pass. For example, if
            ``strings_expected=['a', 'b', 'c']``, then ``'a'`` AND ``'b'`` AND
            ``'c'`` must be in the title for the assertion to pass.
            Alternatively, if ``strings_expected=['a', 'b', ['c', 'd']]``, then
            ``'a'`` AND ``'b'`` AND (at least one of: ``'c'``, ``'d'``) must be
            in the title for the assertion to pass. Case insensitive.
        title_type : string
            One of the following strings ["figure", "axes", "either"]
            `figure`: only the figure title (suptitle) will be tested
            'axes': only the axes title (suptitle) will be tested
            'either': either the figure title or axes title will pass this
            assertion.
            The combined title will be tested.
        message_default : string
            The error message to be displayed if the axis label does not
            contain a string in strings_expected. If `message` contains
            ``'{0}'``, it will be replaced with the first expected string not
            found in the label.
        message_or : string
            Similar to `message_default`, `message_or` is the error message to
            be displated if the axis label does not contain at least one of
            the strings in an inner list in `strings_expected`. If `message`
            contains ``'{0}'``, it will be replaced with the first failing
            inner list in `strings_expected`.
        message_no_title : string
            The error message to be displayed if the expected title is not
            displayed.

        Raises
        -------
        AssertionError
            if title does not contain expected strings
        """
        suptitle, axtitle = self.get_titles()
        if title_type == "either":
            title = axtitle + suptitle
        elif title_type == "figure":
            title = suptitle
        elif title_type == "axes":
            title = axtitle
        else:
            raise ValueError(
                "title_type must be one of the following "
                + '["figure", "axes", "either"]'
            )

        assert title, message_no_title

        self.assert_string_contains(
            title,
            strings_expected,
            message_default=message_default,
            message_or=message_or,
        )

    """CAPTION TEST/HELPER FUNCTIONS """

    def get_caption(self):
        """Returns the text that is located in the bottom right, just below the
        right side of ax
        If no text is found in location, ``None`` is returned.

        Returns
        -------
        caption : string
            the text that is found in bottom right, ``None`` if no text is
            found
        """
        caption = None
        ax_position = self.ax.get_position()
        for tex in self.ax.get_figure().texts:
            tex_position = tex.get_position()
            if (
                ax_position.ymin - 0.1 < tex_position[1] < ax_position.ymin
            ) and (
                ax_position.xmax - 0.5 < tex_position[0] < ax_position.xmax
            ):
                caption = tex
                break
        if isinstance(caption, matplotlib.text.Text):
            caption = caption.get_text()
        return caption

    def assert_caption_contains(
        self,
        strings_expected,
        message_default="Caption does not contain expected string: {0}",
        message_or="Caption does not contain at least one of: {0}",
        message_no_caption="No caption exists in appropriate location",
    ):
        """
        Asserts that caption contains expected strings from `strings_expected`.

        Parameters
        ----------
        strings_expected : list
            Any string in `strings_expected` must be in the title for the
            assertion to pass. If there is a list of strings in
            `strings_expected`, at least one of the strings in that list must
            be in the title for the assertion to pass. For example, if
            ``strings_expected=['a', 'b', 'c']``, then ``'a'`` AND ``'b'`` AND
            ``'c'`` must be in the title for the assertion to pass.
            Alternatively, if ``strings_expected=['a', 'b', ['c', 'd']]``, then
            ``'a'`` AND ``'b'`` AND (at least one of: ``'c'``, ``'d'``) must be
            in the title for the assertion to pass. Case insensitive.
        message_default : string
            The error message to be displayed if the axis label does not
            contain a string in strings_expected. If `message` contains
            ``'{0}'``, it will be replaced with the first expected string
            not found in the label.
        message_or : string
            Similar to `message_default`, `message_or` is the error message to
            be displated if the axis label does not contain at least one of
            the strings in an inner list in `strings_expected`. If `message`
            contains ``'{0}'``, it will be replaced with the first failing
            inner list in `strings_expected`.
        message_no_caption : string
            The error message to be displayed if no caption exists in the
            appropriate location.

        Raises
        -------
        AssertionError
            if caption does not contain strings matching `strings_expected`
        """
        caption = self.get_caption()
        if strings_expected is None:
            return

        assert caption, message_no_caption

        self.assert_string_contains(
            caption,
            strings_expected,
            message_default=message_default,
            message_or=message_or,
        )

    """ AXIS TEST/HELPER FUNCTIONS """

    def assert_axis_off(self, message="Axis lines are displayed on plot"):
        """Asserts one of the three cases holds true with error message m:
        1) axis have been turned off
        2) both x and y axis have visibility set to false
        3) both x and y axis ticks have been set to empty lists

        Parameters
        ----------
        message : string
            The error message to be displayed if the assertion is not met.

        Raises
        ----------
        AssertionError
            with message `m` if axis lines are displayed on plot
        """
        flag = False
        # Case 1: check if axis have been turned off
        if not self.ax.axison:
            flag = True
        # Case 2: Check if both axis visibilities set to false
        elif not self.ax.xaxis._visible and not self.ax.yaxis._visible:
            flag = True
        # Case 3: Check if both axis ticks are set to empty lists
        elif (
            self.ax.xaxis.get_gridlines() == []
            and self.ax.yaxis.get_gridlines() == []
        ):
            flag = True

        assert flag, message

    def assert_axis_label_contains(
        self,
        axis="x",
        strings_expected=None,
        message_default="{1}-axis label does not contain expected string: {0}",
        message_or="{1}-axis label does not contain at least one of: {0}",
        message_not_displayed="Expected {0} axis label is not displayed",
    ):
        """
        Asserts that the axis label contains the expected strings from
        `strings_expected`. Tests x or y axis based on 'axis' param.

        Parameters
        ----------
        axis : string
            One of the following ['x','y'] stated which axis label to be tested
        strings_expected : list
            Any string in `strings_expected` must be in the axis label for the
            assertion to pass. If there is a list of strings in
            `strings_expected`, at least one of the strings in that list must
            be in the axis label for the assertion to pass. For example, if
            ``strings_expected=['a', 'b', 'c']``, then ``'a'`` AND ``'b'`` AND
            ``'c'`` must be in the title for the assertion to pass.
            Alternatively, if ``strings_expected=['a', 'b', ['c', 'd']]``, then
            ``'a'`` AND ``'b'`` AND (at least one of: ``'c'``, ``'d'``) must be
            in the title for the assertion to pass. Case insensitive.
        message_default : string
            The error message to be displayed if the axis label does not
            contain a string in strings_expected. If `message` contains
            ``'{1}'``, it will be replaced with `axis`. If `message` contains
            ``'{0}'``, it will be replaced with the first expected string not
            found in the label.
        message_or : string
            Similar to `message_default`, `message_or` is the error message to
            be displated if the axis label does not contain at least one of
            the strings in an inner list in `strings_expected`. If `message`
            contains ``'{1}'``, it will be replaced with `axis`. If `message`
            contains ``'{0}'``, it will be replaced with the first failing
            inner list in `strings_expected`.
        message_not_displayed : string
            The error message to be displayed if the expected axis label is not
            displayed. If `message_not_displayed` contains ``'{0}'``, it will
            be replaced with `axis`.

        Raises
        ----------
        AssertionError
            if axis label does not contain expected strings
        """
        # Retrieve appropriate axis label, error if axis param is not x or y
        if axis == "x":
            label = self.ax.get_xlabel()
        elif axis == "y":
            label = self.ax.get_ylabel()
        else:
            raise ValueError('axis must be one of the following ["x", "y"]')

        # Check that axis label contains the expected strings in lst
        if strings_expected is None:
            return
        assert label, "Expected {0} axis label is not displayed".format(axis)

        message_default = message_default.replace("{1}", axis)
        message_or = message_or.replace("{1}", axis)
        self.assert_string_contains(
            label,
            strings_expected,
            message_default=message_default,
            message_or=message_or,
        )

    def assert_lims(
        self,
        lims_expected,
        axis="x",
        message="Incorrect limits on the {0} axis",
    ):
        """Assert the lims of ax match lims_expected. Tests x or y axis based on
        'axis' param

        Parameters
        ---------
        lims_expected : list of numbers (float or int)
            List of length 2 containing expected min and max vals for axis
            limits
        axis : string
            From ['x','y'], which axis to be tested
        message : string
            The error message to be displayed if the limits of ax do not match
            the expected limits. If `message` contains ``'{0}'``, it will be
            replaced with `axis`.

        Raises
        ----------
        AssertionError
            if `lims_expected` does not match the limits of ax
        """
        # Get axis limit values
        if axis == "x":
            lims = [int(xlim) for xlim in self.ax.get_xlim()]
        elif axis == "y":
            lims = [int(ylim) for ylim in self.ax.get_ylim()]
        else:
            raise ValueError(
                "axis must be one of the following string ['x', 'y']"
            )

        # Check retrieved limits against expected min and max values
        assert np.array_equal(lims, lims_expected), message.format(axis)

    def assert_lims_range(
        self,
        lims_range,
        axis="x",
        message_min="Incorrect min limit on the {0} axis",
        message_max="Incorrect max limit on the {0} axis",
    ):
        """Asserts axis limits fall within lims_range (INCLUSIVE).

        Parameters
        ----------
        lims_range: tuple of tuples.
            if axis == 'x': first tuple is range the left x limit must be in,
            second tuple is the range the right x limit must be in
            if axis == 'y': first tuple is range the bottom y limit must be in,
            second tuple is the range the top x limit must be in
        axis: string
            from list ['x','y'] declaring which axis to be tested
        message_min : string
            The error message to be displayed if the limits of ax do not fall
            within the expected limit minimum. If `message` contains ``'{0}'``,
            it will be replaced with `axis`.
        message_max : string
            The error message to be displayed if the limits of ax do not fall
            within the expected limit maximum. If `message` contains ``'{0}'``,
            it will be replaced with the specified `axis` (i.e. it will be
            replaced with 'x' or 'y').

        Raises
        ----------
        AssertionError
            if axis limits does not fall within `lims_range`
        """
        # Get ax axis limits
        if axis == "x":
            lims = self.ax.get_xlim()
        elif axis == "y":
            lims = self.ax.get_ylim()
        else:
            raise ValueError(
                "axis must be one of the following string ['x', 'y']"
            )
        # Check if the min falls with in lims_range[0]
        assert (
            lims_range[0][0] <= lims[0] <= lims_range[0][1]
        ), message_min.format(axis)
        # Check if the max falls with in lims_range[1]
        assert (
            lims_range[1][0] <= lims[1] <= lims_range[1][1]
        ), message_max.format(axis)

    def assert_equal_xlims_ylims(
        self, message="xlims and ylims are not equal"
    ):
        """Assert the x and y lims of Axes ax are exactly equal to each other

        Parameters
        ---------
        message : string
            The error message to be displayed if the x limits and y limits are
            equal.

        Raises
        ----------
        AssertionError
            with message `m` if limits are not equal

        """
        xlims = self.ax.get_xlim()
        ylims = self.ax.get_ylim()
        assert np.array_equal(xlims, ylims), message

    """ LEGEND TESTS """

    def get_legends(self):
        """Retrieve the list of legends on ax

        Returns
        -------
        legends : list
            List of matplotlib.legend.Legend objects
        """
        return self.ax.findobj(match=matplotlib.legend.Legend)

    def assert_legend_titles(
        self,
        titles_exp,
        message="Legend title does not contain expected string: {0}",
        message_num_titles="I was expecting {0} legend titles but instead "
        + "found {1}",
    ):
        """Asserts legend titles contain expected text in titles_exp list.

        Parameters
        ----------
        titles_exp : list of strings
            Each string is expected be be in one legend title. The number of
            strings is equal to the number of expected legends.
        message : string
            The error message to be displayed if the legend titles do not match
            the expected strings. If `message` contains ``'{0}'``,
            it will be replaced with the first expected string that does not
            exist in the legend title.
        message_num_titles : string
            The error message to be displayed if there exist a different number
            of legend titles than expected. If `message_num_titles` contains
            ``'{0}'`` it will be replaced with the number of titles found. If
            `message_num_titles` contains ``'{1}'`` it will be replaced with
            the expected number of titles.

        Raises
        -------
        AssertionError
            if legend titles do not contain expected text
        """
        legends = self.get_legends()

        # Test number of legends - edge case when a student might have two
        # legends rather than 2

        num_legends = len(legends)
        num_exp_legends = len(titles_exp)

        assert num_legends == num_exp_legends, message_num_titles.format(
            num_legends, num_exp_legends
        )

        # Check that each expected legend title is in a legend title in ax
        titles = [leg.get_title().get_text().lower() for leg in legends]

        for title_exp in titles_exp:
            assert any(title_exp.lower() in s for s in titles), message.format(
                title_exp
            )

    def assert_legend_labels(
        self,
        labels_exp,
        message="Legend does not have expected labels",
        message_no_legend="Legend does not exist",
        message_num_labels="I was expecting {0} legend entries, but found "
        + "{1}. Are there extra labels in your legend?",
    ):
        """Asserts legends on ax have the correct entry labels

        Parameters
        ----------
        labels_exp : list of strings
            Each string is an expected legend entry label. Checks that
            the legend entry labels match exactly (except for case).
        message : string
            The error message to be displayed if the expected labels are not
            found.
        message_no_legend : string
            The error message to be displayed if no legend is found.
        message_num_labels: string
            The error message to be displayed if there exist a different number
            of legend labels than expected. If `message_num_labels` contains
            ``'{0}'`` it will be replaced with the number of labels found. If
            `message_num_labels` contains ``'{1}'`` it will be replaced with
            the expected number of labels.


        Raises
        -------
        AssertionError
            if legend labeles do not match `labels_exp`

        Notes
        -----
        If there are multiple legends, it combines all the legend labels into
        one set and checks that set against the list labels_exp
        """
        legends = self.get_legends()
        assert legends, message_no_legend

        # Lowercase both the expected and actual legend labels
        legend_texts = [
            t.get_text().lower() for leg in legends for t in leg.get_texts()
        ]
        labels_exp = [label.lower() for label in labels_exp]

        num_exp_labs = len(labels_exp)
        num_actual_labs = len(legend_texts)
        assert num_actual_labs == num_exp_labs, message_num_labels.format(
            num_exp_labs, num_actual_labs
        )
        assert set(legend_texts) == set(labels_exp), message

    def assert_legend_no_overlay_content(
        self, message="Legend overlays plot window"
    ):
        """Asserts that each legend does not overlay plot window

        Parameters
        ----------
        message : string
            The error message to be displayed if the legend overlays the plot
            window.

        Raises
        -------
        AssertionError
            with message `m` if legend does not overlay plot window
        """
        # RendererBase() is needed to get extent, otherwise raises an error
        plot_extent = self.ax.get_window_extent(RendererBase()).get_points()
        legends = self.get_legends()
        for leg in legends:
            # RendererBase() is needed to get extent, otherwise raises error
            leg_extent = leg.get_window_extent(RendererBase()).get_points()
            legend_left = leg_extent[1][0] < plot_extent[0][0]
            legend_right = leg_extent[0][0] > plot_extent[1][0]
            legend_below = leg_extent[1][1] < plot_extent[0][1]
            assert legend_left or legend_right or legend_below, message

    def legends_overlap(self, b1, b2):
        """Helper function for assert_no_legend_overlap.
        True if points of window extents for b1 and b2 overlap, False otherwise

        Parameters
        ----------
        b1 : list of lists
            2x2 array containg numbers, bounding box of window extents
        b2 : list of lists
            2x2 array containg numbers, bounding box of window extents

        Returns
        -------
        overlap : boolean
            True if bounding boxes b1 and b2 overlap
        """
        x_overlap = (b1[0][0] <= b2[1][0] and b1[0][0] >= b2[0][0]) or (
            b1[1][0] <= b2[1][0] and b1[1][0] >= b2[0][0]
        )
        y_overlap = (b1[0][1] <= b2[1][1] and b1[0][1] >= b2[0][1]) or (
            b1[1][1] <= b2[1][1] and b1[1][1] >= b2[0][1]
        )
        return x_overlap and y_overlap

    def assert_no_legend_overlap(self, message="Legends overlap eachother"):
        """When multiple legends on ax, asserts that there are no two legends
        in ax that overlap each other

        Parameters
        ----------
        message : string
            The error message to be displayed if two legends overlap.

        Raises
        -------
        AssertionError
            with message `m` if legends overlap
        """
        legends = self.get_legends()
        n = len(legends)
        for i in range(n - 1):
            # Get extent of first legend in check, RendererBase() avoids error
            leg_extent1 = (
                legends[i].get_window_extent(RendererBase()).get_points()
            )
            for j in range(i + 1, n):
                # Get extent of second legend in check
                leg_extent2 = (
                    legends[j].get_window_extent(RendererBase()).get_points()
                )
                assert not self.legends_overlap(
                    leg_extent1, leg_extent2
                ), message

    """ BASIC PLOT DATA FUNCTIONS """

    def get_xy(self, points_only=False):
        """Returns a pandas dataframe with columns "x" and "y" holding the x
        and y coords on Axes `ax`

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Matplotlib Axes object to be tested
        points_only : boolean
            Set ``True`` to check only points, set ``False`` to check all data
            on plot.

        Returns
        -------
        df : pandas.DataFrame
            Pandas dataframe with columns "x" and "y" containing the x and y
            coords of each point on Axes `ax`
        """
        if points_only:
            xy_coords = [
                val
                for line in self.ax.lines
                if (
                    line.get_linestyle() == "None"
                    or line.get_linewidth() == "None"
                )
                for val in line.get_xydata()
            ]  # .plot()
            xy_coords += [
                val
                for c in self.ax.collections
                if type(c) != matplotlib.collections.PolyCollection
                for val in c.get_offsets()
            ]  # .scatter()

        else:
            xy_coords = [
                val for line in self.ax.lines for val in line.get_xydata()
            ]  # .plot()
            xy_coords += [
                val for c in self.ax.collections for val in c.get_offsets()
            ]  # .scatter()
            xy_coords += [
                [(p.get_x() + (p.get_width() / 2)), p.get_height()]
                for p in self.ax.patches
            ]  # .bar()

        xy_data = pd.DataFrame(data=xy_coords, columns=["x", "y"]).dropna()

        # crop to limits
        lims = self.ax.get_xlim()
        xy_data = xy_data[xy_data["x"] >= lims[0]]
        xy_data = xy_data[xy_data["x"] <= lims[1]].reset_index(drop=True)

        return xy_data

    def assert_xydata(
        self,
        xy_expected,
        xcol=None,
        ycol=None,
        points_only=False,
        xlabels=False,
        tolerance=0,
        message="Incorrect data values",
    ):
        """Asserts that the x and y data of Axes `ax` matches `xy_expected`
        with error message `message`. If ``xy_expected = None``,
        assertion is passed.

        Parameters
        ----------
        xy_expected : pandas or geopandas dataframe
            (Required) DataFrame contains data expected to be on the plot
            (axis object)
        xcol : string
            (Required for non geopandas objects) Title of column in
            `xy_expected` containing values along `x_axis`.
            If `xy_expected` contains this data in 'geometry', set to ``None``.
        ycol : String
            (Required for non geopandas objects) The y column name of
            xy_expected which represents values along the`y_axis` in a plot.
            If `xy_expected` contains this data in 'geometry' set to ``None``.
        points_only : boolean,
            Set ``True`` to check only points, set ``False`` tp check all data
            on plot.
        xlabels : boolean
            Set ``True`` if using x axis labels rather than x data. Instead of
            comparing numbers in the x-column to expected, compares numbers or
            text in x labels to expected.
        tolerance : float
            A non-zero value of tol_rel allows an absolute tolerance when
            checking the data. For example, a tolerance of 0.1 would
            check that the actual data is within 0.1 units of the actual data.
            Note that the units for datetime data is always days.
        message : string
            The error message to be displayed if the xy-data does not match
            `xy_expected`


        Raises
        -------
        AssertionError
            with message `message`, if x and y data of Axes `ax` does not match
            `xy_expected`
        """
        if xy_expected is None:
            return
        elif not isinstance(xy_expected, pd.DataFrame):
            raise ValueError(
                "xy_expected must be of type: pandas dataframe or Geopandas "
                + "Dataframe"
            )

        # If xy_expected is a GeoDataFrame, then we make is a normal DataFrame
        # with the coordinates of the geometry in that GeoDataFrame as the x
        # and y data
        if isinstance(xy_expected, gpd.geodataframe.GeoDataFrame) and not xcol:
            xy_expected = pd.DataFrame(
                data={
                    "x": [p.x for p in xy_expected.geometry],
                    "y": [p.y for p in xy_expected.geometry],
                }
            ).dropna()
            xcol, ycol = "x", "y"

        if xlabels:
            self.assert_xlabel_ydata(
                xy_expected, xcol=xcol, ycol=ycol, message=message
            )
            return
        xy_data = self.get_xy(points_only=points_only)

        # Make sure the data are sorted the same
        xy_data, xy_expected = (
            xy_data.sort_values(by="x"),
            xy_expected.sort_values(by=xcol),
        )

        if tolerance > 0:
            np.testing.assert_allclose(
                xy_data["x"],
                xy_expected[xcol],
                atol=tolerance,
                err_msg=message,
            )
            np.testing.assert_allclose(
                xy_data["y"],
                xy_expected[ycol],
                atol=tolerance,
                err_msg=message,
            )

        else:
            """We use `assert_array_max_ulp()` to compare the
            two datasets because it is able to account for small errors in
            floating point numbers, and it scales nicely between extremely
            small or large numbers. Because of the way that matplotlib stores
            datetime data, this is essential for comparing high-precision
            datetime data (i.e. millisecond or lower).

            We catch this error and raise our own that is more relevant to
            the assertion being run."""
            try:
                np.testing.assert_array_max_ulp(
                    xy_data["x"].to_numpy(dtype=np.float64),
                    xy_expected[xcol].to_numpy(dtype=np.float64),
                    5,
                )
            except AssertionError:
                # xy_data and xy_expected do not contain the same data
                raise AssertionError(message)
            except ValueError:
                # xy_data and xy_expected do not have the same shape
                raise ValueError(
                    "xy_data and xy_expected do not have the same shape"
                )
            try:
                np.testing.assert_array_max_ulp(
                    xy_data["y"].to_numpy(dtype=np.float64),
                    xy_expected[ycol].to_numpy(dtype=np.float64),
                    5,
                )

            except AssertionError:
                # xy_data and xy_expected do not contain the same data
                raise AssertionError(message)
            except ValueError:
                # xy_data and xy_expected do not have the same shape
                raise ValueError(
                    "xy_data and xy_expected do not have the same shape"
                )

    def assert_xlabel_ydata(
        self, xy_expected, xcol, ycol, message="Incorrect Data"
    ):
        """Asserts that the numbers in x labels and y values in Axes `ax` match
        `xy_expected`.

        Parameters
        ----------
        xy_expected : pandas.DataFrame
            Pandas DataFrame that contains data
        xcol : string
            Column title containing xaxis data
        ycol : string
            Column title containing yaxis data
        message : string
            The error message to be displayed if data in the x-labels and
            y-values do not match `xy_expected`.

        Raises
        -------
        AssertionError
            with message `m` if legends overlap

        Notes
        -----
        This is only testing the numbers in x-axis labels.
        """
        x_data = [
            "".join(c for c in label.get_text())
            for label in self.ax.xaxis.get_majorticklabels()
        ]
        y_data = self.get_xy()["y"]
        xy_data = pd.DataFrame(data={"x": x_data, "y": y_data})

        # If we expect x-values to be numbers
        if all([isinstance(i, numbers.Number) for i in xy_expected[xcol]]):
            x_is_numeric = True
            try:
                x_data_numeric = [float(i) for i in xy_data["x"]]
            except ValueError:
                raise AssertionError(message)
            else:
                xy_data["x"] = x_data_numeric

        # If we expect x-values to be strings
        else:
            # If we expect x-values to be numeric strings
            if all([s.isnumeric() for s in xy_expected[xcol]]):
                # We attempt to convert numeric strings to numbers
                try:
                    x_expected = [float(s) for s in xy_expected[xcol]]
                    x_data = [float(s) for s in xy_data["x"]]
                except ValueError:
                    x_is_numeric = False
                else:
                    x_is_numeric = True
                    xy_expected[xcol] = x_expected
                    xy_data["x"] = x_data
            # We expect x-values to be non-numeric strings
            else:
                x_is_numeric = False

        # Testing x-data
        if x_is_numeric:
            try:
                np.testing.assert_array_max_ulp(
                    np.array(xy_data["x"]),
                    np.array(xy_expected[xcol]),
                )
            except AssertionError:
                raise AssertionError(message)
        else:
            np.testing.assert_equal(
                np.array(xy_data["x"]), np.array(xy_expected[xcol]), message
            )

        # Testing y-data
        try:
            np.testing.assert_array_max_ulp(
                np.array(xy_data["y"]), np.array(xy_expected[ycol])
            )
        except AssertionError:
            raise AssertionError(message)

    # LINE TESTS/HELPER FUNCTIONS

    def get_slope_yintercept(self, path_verts):
        """Returns the y-intercept of line based on the average slope of the
        line

        Parameters
        ----------
        path_verts : list
            List of verticies that make a line on Axes `ax`

        Returns
        -------
        slope : float
            The average slope of the line defined by `path_verts`
        y_intercept : float
            The y intercept of the line defined by `path_verts`
        """
        slopes = [
            (path_verts[i + 1, 1] - path_verts[i, 1])
            / (path_verts[i + 1, 0] - path_verts[i, 0])
            for i in range(len(path_verts) - 1)
        ]
        slope = sum(slopes) / len(slopes)
        return slope, path_verts[0, 1] - (path_verts[0, 0] * slope)

    def assert_line(
        self,
        slope_exp,
        intercept_exp,
        check_coverage=True,
        message_no_line="Expected line not displayed",
        message_data="Line does not cover data set",
    ):
        """Asserts that there exists a line on Axes `ax` with slope `slope_exp`
        and y-intercept `intercept_exp` and

        Parameters
        ----------
        slope_exp : float
            Expected slope of line
        intercept_exp : float
            Expeted y intercept of line
        check_coverage : boolean (default = True)
            If `check_coverage` is `True`, function will check that the goes at
            least from x coordinate `min_val` to x coordinate `max_val`. If the
            line does not cover the entire dataset, and `AssertionError` with
            be thrown with message `message_data`.
        message_no_line : string
            The error message to be displayed if the line does not exist.
        message_data : string
            The error message to be displayed if the line exists but does not
            cover the dataset, and if `check_coverage` is `True`.

        Raises
        -------
        AssertionError
            with message `message_no_line` or `message_data` if no line exists
            that covers the dataset.
        """
        flag_exist = False

        if check_coverage:
            flag_length = False
            xy = self.get_xy(points_only=True)
            min_val, max_val = min(xy["x"]), max(xy["x"])

        for line in self.ax.lines:
            # Here we will get the verticies for the line and reformat them in

            # the way that get_slope_yintercept() expects
            data = line.get_data()
            path_verts = np.column_stack((data[0], data[1]))

            slope, y_intercept = self.get_slope_yintercept(path_verts)
            if math.isclose(slope, slope_exp, abs_tol=1e-4) and math.isclose(
                y_intercept, intercept_exp, abs_tol=1e-4
            ):
                flag_exist = True
                line_x_vals = [coord[0] for coord in path_verts]

                # This check ensures that the minimum and maximum values of the
                # line are within or very close to the minimum and maximum
                # values in the pandas dataframe provided. This accounts for
                # small errors sometimes found in matplotlib plots.
                if check_coverage:
                    if (
                        math.isclose(min(line_x_vals), min_val, abs_tol=1e-4)
                        or min(line_x_vals) <= min_val
                    ) and (
                        math.isclose(max(line_x_vals), max_val, abs_tol=1e-4)
                        or max(line_x_vals) >= max_val
                    ):
                        flag_length = True
                        break

        assert flag_exist, message_no_line
        if check_coverage:
            assert flag_length, message_data

    def assert_lines_of_type(self, line_types, check_coverage=True):
        """Asserts each line of type in `line_types` exist on `ax`

        Parameters
        ----------
        line_types : string or list of strings
            Acceptable strings in line_types are as follows
            ``['linear-regression', 'onetoone']``.
        check_coverage : boolean (default = True)
            If `check_coverage` is `True`, function will check that the goes at
            least from x coordinate `min_val` to x coordinate `max_val`. If the
            line does not cover the entire dataset, and `AssertionError` with
            be thrown with message `message_data`.

        Raises
        -------
        AssertionError
            if at least one line of type in `line_types` does not exist on `ax`

        Notes
        -----
            If `line_types` is empty, assertion is passed.
        """
        if isinstance(line_types, str):
            line_types = [line_types]

        for line_type in line_types:
            if line_type == "linear-regression":
                xy = self.get_xy(points_only=True)
                # Check that there is xy data for this line. Some one-to-one
                # lines do not produce xy data.
                if xy.empty:
                    raise AssertionError(
                        "linear-regression line not displayed properly"
                    )
                slope_exp, intercept_exp, _, _, _ = stats.linregress(
                    xy.x, xy.y
                )
            elif line_type == "onetoone":
                slope_exp, intercept_exp = 1, 0
            else:
                raise ValueError(
                    "each string in line_types must be from the following "
                    + '["linear-regression","onetoone"]'
                )

            self.assert_line(
                slope_exp,
                intercept_exp,
                message_no_line="{0} line not displayed properly".format(
                    line_type
                ),
                message_data="{0} line does not cover dataset".format(
                    line_type
                ),
                check_coverage=check_coverage,
            )

    # HISTOGRAM FUNCTIONS

    def get_num_bins(self):
        """Gets the number of bins in histogram with a unique x-position.

        Returns
        -------
        Int :
            Returns the number of bins with a unique x-position. For a normal
            histogram, this is just the number of bins. If there are two
            overlapping or stacked histograms in the same
            `matplotlib.axis.Axis` object, then this returns the number of bins
            with unique edges."""
        x_data = self.get_xy()["x"]
        unique_x_data = list(set(x_data))
        num_bins = len(unique_x_data)

        return num_bins

    def assert_num_bins(
        self,
        num_bins,
        message="Expected {0} bins in histogram, instead found {1}.",
    ):
        """Asserts number of bins is `num_bins`.

        Parameters
        ----------
        num_bins : int
            Number of bins expected.
        message : string
            The error message to be displayed if plot does not contain
            `num_bins`. If `message` contains ``'{0}'`` it will be replaced
            with expected number of bins. If `message` contains ``'{1}'``, it
            will be replaced with the number of bins found.

        Raises
        -------
        AssertionError
            if plot does not contain the expected number of bins
        """

        num_bins_found = self.get_num_bins()

        assert num_bins == num_bins_found, message.format(
            num_bins, num_bins_found
        )

    def get_bin_values(self):
        """Returns the value of each bin in a histogram (i.e. the height of each
        bar in a histogram.)

        Returns
        -------
        Int :
            The number of bins in the histogram"""

        bin_values = self.get_xy()["y"].tolist()

        return bin_values

    def get_bin_midpoints(self):
        """Returns the mid point value of each bin in a histogram

        Returns
        -------
        Int :
            The number of bins in the histogram"""

        bin_midpoints = self.get_xy()["x"].tolist()

        return bin_midpoints

    def assert_bin_values(
        self,
        bin_values,
        tolerance=0,
        message="Did not find expected bin values in plot",
    ):
        """Asserts that the values of histogram bins match `bin_values`.

        Parameters
        ----------
        bin_values : list
            A list of numbers representing the expected values of each
            consecutive bin (i.e. the heights of the bars in the histogram).
        tolerance : float
            A non-zero value of tol_abs allows an absolute tolerance when
            checking the bin values. For example, an absolute tolerance of 1
            checks that the actual bin values do not differ from the expected
            bin values by more than 1.
        message : string
            The error message to be displayed if the bin values do not match
            `bin_values`

        Raises
        ------
        AssertionError
            if the Values of histogram bins do not match `bin_values`


        Notes
        -----
            `bin_values` can be difficult to know. The easiest way to obtain
            them may be to create a histogram with your expected data, create a
            `PlotTester` object, and use ``get_bin_values()``.
            ``get_bin_values()`` will return exactly the type of list required
            for `bin_values` in this method.
        """
        expected_bin_values = bin_values
        plot_bin_values = self.get_bin_values()

        if tolerance > 0:
            try:
                np.testing.assert_allclose(
                    plot_bin_values,
                    expected_bin_values,
                    atol=tolerance,
                    err_msg=message,
                )
            except AssertionError:
                raise AssertionError(message)
        else:
            """We use `assert_array_max_ulp()` to compare the
            two datasets because it is able to account for small errors in
            floating point numbers, and it scales nicely between extremely
            small or large numbers. We catch this error and throw our own so
            that we can use our own message."""
            try:
                np.testing.assert_array_max_ulp(
                    np.array(plot_bin_values), np.array(expected_bin_values)
                )
            except AssertionError:
                raise AssertionError(message)

    def assert_bin_midpoints(
        self,
        bin_midpoints,
        message="Did not find expected bin midpoints in plot",
    ):
        """
        Asserts that the middle values of histogram bins match `bin_midpoints`.

        Parameters
        ----------
        bin_midpoints : list
            A list of numbers representing the expected middles of bin values
            covered by each consecutive bin (i.e. the midpoint of the bars in
            the histogram).
        message : string
            The error message to be displayed if the bin mid point values do
            not match `bin_midpoints`

        Raises
        ------
        AssertionError
            if the Values of histogram bins do not match `bin_midpoints`
        """

        plot_bin_midpoints = self.get_bin_midpoints()

        if not isinstance(bin_midpoints, list):
            raise ValueError(
                "Need to submit a list for expected bin midpoints."
            )

        if len(plot_bin_midpoints) != len(bin_midpoints):
            raise ValueError("Bin midpoints lists lengths do no match.")

        try:
            np.testing.assert_array_max_ulp(
                np.array(plot_bin_midpoints), np.array(bin_midpoints)
            )
        except AssertionError:
            raise AssertionError(message)
