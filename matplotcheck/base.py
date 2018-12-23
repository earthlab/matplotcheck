import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib
import math
from scipy import stats


class InvalidPlotError(Exception):
    pass


class PlotTester(object):
    """Object to test Matplotlib plots

    Parameters
    ----------
    axis: Matplotlib.Axes.axes object
    """

    def __init__(self, ax):
        """Initialize TestPlot object"""
        self.ax = ax

    def _is_line(self):
        """Boolean expressing if ax contains scatter points.
        If plot contains scatter points as well as lines, functions will return true.

        Returns
        -------
        boolean: True if Axes ax is a scatter plot, False if not
        """

        if self.ax.lines:
            for l in self.ax.lines:
                if (
                    not l.get_linestyle()
                    or not l.get_linewidth()
                    or l.get_linewidth() > 0
                ):
                    return True

    def _is_scatter(self):
        """Boolean expressing if ax contains scatter points.
        If plot contains scatter points as well as lines, functions will return true.

        Returns
        -------
        boolean: True if Axes ax is a scatter plot, False if not
        """
        if self.ax.collections:
            return True
        elif self.ax.lines:
            for l in self.ax.lines:
                if (
                    l.get_linestyle() == "None"
                    or l.get_linewidth() == "None"
                    or l.get_linewidth() == 0
                ):
                    return True
        return False

    def assert_plot_type(self, plot_type=None):
        """Asserts Axes ax contains the type of plot specified in plot_type.
        if plot_type is None, assertion is passed

        Parameters
        ----------
        plot_type: string
            String specifying the expected plot type. Options: 'scatter','bar', 'line'
        """
        if plot_type:
            if plot_type == "scatter":
                assert self._is_scatter(), "Plot is not of type {0}".format(
                    plot_type
                )
            elif plot_type == "bar":
                assert self.ax.patches, "Plot is not of type {0}".format(
                    plot_type
                )
            elif plot_type == "line":
                assert self._is_line(), "Plot is not of type {0}".format(
                    plot_type
                )
            else:
                raise ValueError(
                    "plot_type must be on of the following string ['scatter', 'bar' or 'line']"
                )

    ## TITLES TESTS/HELPER FUNCTIONS ##

    def get_titles(self):
        """Returns the suptitle (Figure title) and axes title of ax

        Returns
        -------
        suptitle: string
            Figure title of the Figure that the ax object is on. If none, this is an empty string
        title: title on the axes. If none, this is an empty string.
        """
        fig, suptitle = self.ax.get_figure(), ""
        if fig._suptitle:
            suptitle += fig._suptitle.get_text()
        return suptitle, self.ax.get_title()

    def assert_title_contains(self, lst, title_type="either"):
        """Asserts title contains each string in lst. Whether we test the axes title or figure title
            is described in title_type.

        Parameters
        ----------
        lst: list
            list of strings to be searched for in title. strings must be lower case.
        title_type: string
            one of the following strings ["figure", "axes", "either"]
            `figure`: only the figure title (suptitle) will be tested
            'axes': only the axes title (suptitle) will be tested
            'either': either the figure title or axes title will pass this assertion.
            The combined title will be tested.
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
                'title_type must be one of the following ["figure", "axes", "either"]'
            )

        if lst == None:
            pass
        else:
            assert title, "Expected title is not displayed"
            title = title.lower().replace(" ", "")
            for s in lst:
                assert (
                    s.lower().replace(" ", "") in title
                ), "Title does not contain expected text:{0}".format(s)

    ## CAPTION TEST/HELPER FUNCTIONS ##

    def get_caption(self):
        """Returns matplotlib.text.Text that is located in the bottom right, just below the right side of ax
            If no text is found in location, None is returned.

        Returns
        -------
        matplotlib.text.Text if text is found in bottom right. None if no text is found in said location.
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
        return caption

    def assert_caption_contains(self, strings_exp):
        """Asserts that Axes ax contains strings as expected in strings_exp.
            strings_exp is a list of lists. Each internal list is a list of strings where at least one string
            must be in the caption, barring capitalization. Once a string is found, it is removed from the caption,
            therefore, order does matter. This is to enforce no overlap in found strings.

        Parameters
        ----------
        strings_exp: list of lists. Each internal list is a list of strings where at least one string must be
            found in the caption. Input strings must be lower case, as we are not testing for capitalization
            if None: assert caption does not exist
            if empty list: asserts caption exists and not an empty string
        """
        caption = self.get_caption()
        if strings_exp == None:
            return
        else:
            assert caption, "No caption exist in appropriate location"

        caption = caption.get_text().lower().replace(" ", "")
        for lst in strings_exp:
            flag = False
            for s in lst:
                if s.lower().replace(" ", "") in caption:
                    caption = caption.replace(s, "")
                    flag = True
                    break
            assert (
                flag
            ), "Caption does not contain expected string: {0}".format(s)

    ## AXIS TEST/HELPER FUNCTIONS ##

    def assert_axis_off(self, m="Axis lines are displayed on plot"):
        """Asserts one of the three cases holds true with error message m:
        1) axis have been turned off
        2) both x and y axis have visibility set to false
        3) both x and y axis ticks have been set to empty lists

        Parameters
        ----------
        m: string error message if assertion is not met
        """
        flag = False
        if self.ax.axison == False:
            flag = True
        elif (
            self.ax.xaxis._visible == False and self.ax.yaxis._visible == False
        ):
            flag = True
        elif (
            self.ax.xaxis.get_gridlines() == []
            and self.ax.yaxis.get_gridlines() == []
        ):
            flag = True
        assert flag, m

    def assert_axis_label_contains(self, axis="x", lst=[]):
        """Asserts axis label contains each of the strings in lst. The axis
        that is tested is described in axis.

        If lst is an empty list, test asserts axis label is not an empty string
        If list is `None`, test assert axis label is an empty string

        Parameters
        ---------
        axis: string
            one of the following ['x','y'] stated which axis label to be tested
        lst: list of strings
            Strings to be searched for in axis label. Strings must be lower case.
        """
        if axis == "x":
            label = self.ax.get_xlabel()
        elif axis == "y":
            label = self.ax.get_ylabel()
        else:
            raise ValueError('axis must be one of the following ["x", "y"]')

        if lst is None:
            pass
        else:
            assert label, "Expected {0} axis label is not displayed".format(
                axis
            )
            label = label.lower().replace(" ", "")
            for s in lst:
                assert (
                    s.lower().replace(" ", "") in label
                ), "{0} axis label does not contain expected text:{1}".format(
                    axis, label
                )

    def assert_lims(self, lims_expected, axis="x"):
        """Assert the lims of ax match lims_expected. Whether this tests the
        x or y axis is denoted in variable axis

        Parameters
        ---------
        lims_expected: list
            list of length 2 containing expected min and max for x axis limits
        axis: string
            from ['x','y'], stated which axis to be tested
        """
        if axis == "x":
            lims = [int(l) for l in self.ax.get_xlim()]
        elif axis == "y":
            lims = [int(l) for l in self.ax.get_ylim()]
        else:
            raise ValueError(
                "axis must be one of the following string ['x', 'y']"
            )
        assert np.array_equal(
            lims, lims_expected
        ), "Incorrect limits on the {0} axis".format(axis)

    def assert_lims_range(self, lims_range, axis="x"):
        """Assers limits along axis defined in variable axis are in range lims_range.

        Parameters
        ----------
        lims_range: tuple of tuples.
            if axis == 'x': first tuple is range the left x limit must be in,
            second tuple is the range the right x limit must be in
            if axis == 'y': first tuple is range the bottom y limit must be in,
            second tuple is the range the top x limit must be in
        axis: string
            from list ['x','y'] declaring which axis to be tested
        """
        if axis == "x":
            lims = self.ax.get_xlim()
        elif axis == "y":
            lims = self.ax.get_ylim()
        else:
            raise ValueError(
                "axis must be one of the following string ['x', 'y']"
            )
        assert lims_range[0][0] < lims[0] < lims_range[0][1]
        assert lims_range[1][0] < lims[1] < lims_range[1][1]

    def assert_equal_xlims_ylims(
        self, message="xlims and ylims are not equal"
    ):
        """Assert the x and y lims of Axes ax are equal to each other

        Parameters
        ---------
        message: string
            Error message if assertion is not met that is shown to the user.
        """
        xlims = self.ax.get_xlim()
        ylims = self.ax.get_ylim()
        assert np.array_equal(xlims, ylims), message

    """ LEGEND TESTS """

    def get_legends(self):
        """Returns a list of legends on ax

        Returns
        -------
        list of matplotlib.legend.Legend objects
        """
        return self.ax.findobj(match=matplotlib.legend.Legend)

    def assert_legend_titles(self, titles_exp):
        """Asserts legend contains subtitles expressed in titles_exp.

        Parameters
        ---------
        titles_exp: list of strings.
            Each string is expected be be in one subtitle. The number of strings is equal
            to the number of expected subtitles.
        """
        legends = self.get_legends()
        assert len(legends) == len(
            titles_exp
        ), "Incorrect number of legend exist"

        titles = [leg.get_title().get_text().lower() for leg in legends]
        for title_exp in titles_exp:
            assert any(
                title_exp in s for s in titles
            ), "Legend subtitle does not contain expected string: {0}".format(
                title_exp
            )

    def assert_legend_labels(self, labels_exp):
        """Asserts legend on ax has the correct entry labels

        Parameters
        ---------
        labels_exp: list of lower case strings.
            Each string is an expected legend entry label.
        """
        legends = self.get_legends()
        assert legends, "Legend does not exist"

        legend_texts = [
            t.get_text().lower() for leg in legends for t in leg.get_texts()
        ]
        assert len(legend_texts) == len(
            labels_exp
        ), "Legend does not contain expected number of entries"
        assert set(legend_texts) == set(
            labels_exp
        ), "Legend does not have expected labels"

    def which_label(self, label, all_label_options):
        """helper function for assert_legend_accuracy_classified_image
        Returns string that represents a category label for label.

        Parameters
        ----------
        label: string
            to see if it contains an option in all_label_options
        all_label_options: list of lists.
            Each internal list represents a classification category.
            Said list is a list of strings where at least one string is
            expected to be in the legend label for this category.

        Returns
        ------
        string that is the first entry in the list which label is matched with.
        If no match is found, return value is None
        """
        for label_opts in all_label_options:
            for s in label_opts:
                if s in label:
                    return label_opts[0]
        return None

    def assert_legend_accuracy_classified_image(
        self, im_expected, all_label_options
    ):
        """Asserts legend correctly describes classified image on Axes ax

        Parameters
        ----------
        im_expected: array of arrays with expected classified image on ax.
            Classification must start with bin 0.
        all_label_options: list of lists.
            Each internal list represents a classification category.
            Said list is a list of strings where at least one string is
            expected to be in the legend label for this category.
        Internal lists must be in the same order as bins in im_expected.
        """
        im_data = []
        if self.ax.get_images():
            im = self.ax.get_images()[0]
            im_data, im_cmap = im.get_array(), im.get_cmap()
        assert list(im_data), "No Image Displayed"

        legends = self.get_legends()
        assert legends, "No legend displayed"

        all_labels_temp = all_label_options
        legend_dict = {}
        for p in [
            p
            for sublist in [leg.get_patches() for leg in legends]
            for p in sublist
        ]:
            label = p.get_label().lower()
            legend_dict[p.get_facecolor()] = which_label(
                label, all_label_options
            )
        assert len([val for val in legend_dict.values() if val]) == len(
            all_label_options
        ), "Incorrect legend labels"

        im_class_dict = {}
        for val in np.unique(im_data):
            im_class_dict[val] = legend_dict[im_cmap(im.norm(val))]
        im_data_labels = [
            [im_class_dict[val] for val in row] for row in im_data.data
        ]
        im_expected_labels = [
            [all_label_options[val][0] for val in row] for row in im_expected
        ]
        assert np.array_equal(
            im_data_labels, im_expected_labels
        ), "Incorrect legend to data relation"

    def assert_legend_no_overlay_content(
        self, m="Legend overlays plot contents"
    ):
        """Asserts that each legend does not overlay plot contents with error message m

        Parameters
        ---------
        m: string error message if assertion is not met
        """
        plot_extent = self.ax.get_window_extent().get_points()
        legends = self.get_legends()
        for leg in legends:
            leg_extent = leg.get_window_extent().get_points()
            legend_left = leg_extent[1][0] < plot_extent[0][0]
            legend_right = leg_extent[0][0] > plot_extent[1][0]
            legend_below = leg_extent[1][1] < plot_extent[0][1]
            assert legend_left or legend_right or legend_below, m

    def legends_overlap(self, b1, b2):
        """Helper function for assert_no_legend_overlap.
        Boolean value if points of window extents for b1 and b2 overlap

        Parameters
        ----------
        b1: bounding box of window extents
        b2: bounding box of window extents

        Returns
        -------
        boolean value that says if bounding boxes b1 and b2 overlap
        """
        x_overlap = (b1[0][0] <= b2[1][0] and b1[0][0] >= b2[0][0]) or (
            b1[1][0] <= b2[1][0] and b1[1][0] >= b2[0][0]
        )
        y_overlap = (b1[0][1] <= b2[1][1] and b1[0][1] >= b2[0][1]) or (
            b1[1][1] <= b2[1][1] and b1[1][1] >= b2[0][1]
        )
        return x_overlap and y_overlap

    def assert_no_legend_overlap(self, m="Legends overlap eachother"):
        """Asserts there are no two legends in Axes ax that overlap each other with error message m

        Parameters
        ----------
        m: string error message if assertion is not met
        """
        legends = self.get_legends()
        n = len(legends)
        for i in range(n - 1):
            leg_extent1 = legends[i].get_window_extent().get_points()
            for j in range(i + 1, n):
                leg_extent2 = legends[j].get_window_extent().get_points()
                assert legends_overlap(leg_extent1, leg_extent2) == False, m

    ## BASIC PLOT DATA FUNCTIONS ##

    def get_xy(self, points_only=False, xtime=False):
        """Returns a pandas dataframe with columns "x" and "y" holding the x and y coords on Axes ax

        PARAMETERS
        ---------
        ax: Matplotlib Ax object
            axes object to be tested
        points_only: boolean
        xtime: boolean
            True if the x axis of the plot contains datetime values

        RETURNS
        -------
        Pandas dataframe with columns "x" and "y" containing the x and y coords of each point on Axes ax
        """
        if points_only:
            xy_coords = [
                val
                for l in self.ax.lines
                if (l.get_linestyle() == "None" or l.get_linewidth() == "None")
                for val in l.get_xydata()
            ]  # .plot()
            xy_coords += [
                val
                for c in self.ax.collections
                if type(c) != matplotlib.collections.PolyCollection
                for val in c.get_offsets()
            ]  # .scatter()

        else:
            xy_coords = [
                val for l in self.ax.lines for val in l.get_xydata()
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

        # change to datetime dtype if needed
        if xtime:
            xy_data["x"] = mdates.num2date(xy_data["x"])
        return xy_data

    def assert_xydata(
        self,
        xy_expected,
        xcol=None,
        ycol=None,
        points_only=False,
        xtime=False,
        xlabels=False,
        tolerence=0,
        m="Incorrect data values",
    ):
        """Asserts that the x and y data of Axes ax matches xy_expected with error message m.
        If xy_expected is None, assertion is passed

        Parameters
        ----------
        ax: Matplotlib Axes object (Required)
            Axis object to be tested
        xy_expected: pandas or geopandas dataframe (Required)
            DF contains data expected to be on the plot (axis object)
        xcol: String (Required for non geopandas objects)
            Title of column in xy_expected containing values along x_axis.
            If xy_expected contains this data in 'geometry', set to None
        ycol: String (Required for non geopandas objects)
            The y column name of xy_expected which represents values along
            the y_axis in a plot.
            If xy_expected contains this data in 'geometry' set to None
        points_only: boolean,
            True if checking only points, false if checking all data on plot
        xtime: boolean
            True if the a-axis contains datetime values. Matplotlib converts
            datetime objects to seconds? This parameter will ensure the provided
            x col values are converted if they are datetime elements.
        xlabels: boolean
            if using x axis labels rather than x data
        tolerence: measure of relative error allowed.
            For example, a value of .001 asserts values in array
            are within .001 of each other. ## this isn't exactly correct.. ##
        m: string
            error message provided to the student if assertion fails
        """

        if type(xy_expected) == gpd.geodataframe.GeoDataFrame and not xcol:
            xy_expected = pd.DataFrame(
                data={
                    "x": [p.x for p in xy_expected.geometry],
                    "y": [p.y for p in xy_expected.geometry],
                }
            ).dropna()
            xcol, ycol = "x", "y"
        if (
            type(xy_expected) == pd.DataFrame
            or type(xy_expected) == gpd.geodataframe.GeoDataFrame
        ):
            if xlabels:
                self.assert_xlabel_ydata(xy_expected, xcol=xcol, ycol=ycol)
                return
            xy_data = self.get_xy(points_only=points_only, xtime=xtime)
            xy_data, xy_expected = (
                xy_data.sort_values(by="x"),
                xy_expected.sort_values(by=xcol),
            )
            if tolerence > 0:
                if xtime:
                    raise ValueError(
                        "tolerence must be 0 with datetime on x-axis"
                    )
                np.testing.assert_allclose(
                    xy_data["x"], xy_expected[xcol], rtol=tolerence, err_msg=m
                )
                np.testing.assert_allclose(
                    xy_data["y"], xy_expected[ycol], rtol=tolerence, err_msg=m
                )
            else:
                assert np.array_equal(xy_data["x"], xy_expected[xcol]), m
                assert np.array_equal(xy_data["y"], xy_expected[ycol]), m
        elif xy_expected == None:
            pass
        else:
            raise ValueError(
                "xy_expected must be of type: pandas dataframe or Geopandas Dataframe"
            )

    def assert_xlabel_ydata(self, xy_expected, xcol, ycol, m="Incorrect Data"):
        """Asserts that the numbers in x labels and y values in Axes ax match xy_expected with error message m.
        Note, this is only testing the numbers in x axis labels.

        Parameters
        ----------
        xy_expected: pandas dataframe that contains data
        xcol: string column title containing xaxis data
        ycol: string column title containing yaxis data
        m: string error message if assertion is not met
        """
        x_data = [
            "".join(c for c in l.get_text() if c.isdigit())
            for l in self.ax.xaxis.get_majorticklabels()
        ]
        y_data = self.get_xy()["y"]
        xy_data = pd.DataFrame(data={"x": x_data, "y": y_data})
        xy_expected, xy_data = (
            xy_expected.sort_values(by=xcol),
            xy_data.sort_values(by="x"),
        )
        np.testing.assert_equal(
            np.array(xy_data["x"]), np.array(xy_expected[xcol]), m
        )
        np.testing.assert_equal(
            np.array(xy_data["y"]), np.array(xy_expected[ycol]), m
        )

    ### LINE TESTS/HELPER FUNCTIONS ###

    def get_slope_yintercept(self, path_verts):
        """Returns the y intercept of line based on the average slope of the line

        Parameters
        ---------
        path_verts: array of verticies that make a line on Axes ax

        Returns
        --------
        slope: float of the average slope
        y_intercept: float of the y intercept
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
        xtime=False,
        m="Expected line not displayed",
        m2="Line does not cover data set",
    ):
        """Asserts that there exists a line on Axes ax with slope slope_exp and y intercept intercept_exp and goes at least from x coordinate min_val to x coordinate max_val

        Parameters
        ---------
        slope_exp: expected slope of line
        intercept_exp: expeted y intercept of line
        xtime: boolean if x-axis values are datetime
        m: error message if line does not exist
        m2: error message if line exist but does not cover data set
        """
        flag_exist, flag_length = False, False
        xy = self.get_xy(points_only=True)
        min_val, max_val = min(xy["x"]), max(xy["x"])

        for l in self.ax.lines:
            path_verts = self.ax.transData.inverted().transform(
                l._transformed_path.get_fully_transformed_path().vertices
            )
            slope, y_intercept = self.get_slope_yintercept(path_verts)
            if math.isclose(slope, slope_exp, abs_tol=1e-4) and math.isclose(
                y_intercept, intercept_exp, abs_tol=1e-4
            ):
                flag_exist = True
                line_x_vals = [coord[0] for coord in path_verts]
                if min(line_x_vals) <= min_val and max(line_x_vals) >= max_val:
                    flag_length = True
                    break

        assert flag_exist, m
        assert flag_length, m2

    def assert_lines_of_type(self, line_types):
        """Asserts each line of type in line_types exist on ax

        Parameters
        ----------
        line_types: list of strings. Acceptable strings in line_types are as follows ['regression', 'onetoone'].
            if list is empty, assert is passed
        """
        if line_types:
            for line_type in line_types:
                if line_type == "regression":
                    xy = self.get_xy(points_only=True)
                    slope_exp, intercept_exp, _, _, _ = stats.linregress(
                        xy.x, xy.y
                    )
                elif line_type == "onetoone":
                    slope_exp, intercept_exp = 1, 0
                else:
                    raise ValueError(
                        'each string in line_types must be from the following ["regression","onetoone"]'
                    )

                self.assert_line(
                    slope_exp,
                    intercept_exp,
                    m="{0} line is not displayed properly".format(line_type),
                    m2="{0} line does not cover dataset".format(line_type),
                )

    ## HISTOGRAM FUCNTIONS ##

    def assert_num_bins(self, n=3, which_bins="positive"):
        """Asserts number of bins of type which_bins is at least n

        Parameters
        --------
        n: int declaring minimum number of bins of type which_bin
        which_bins: string from list ['negative', 'positive']
            'negative': all bins with values centered at a positive value
            'positite': all bins with values centered at a negative value

        Returns
        --------
        """
        x_data = self.get_xy(xtime=False)["x"]
        if which_bins == "negative":
            n_bins = len(x_data[x_data < 0])
        elif which_bins == "positive":
            n_bins = len(x_data[x_data > 0])
        else:
            raise ValueError(
                "which_bins must be from list ['negative', 'positive']"
            )
        assert n_bins >= n, "Not enough {0} value bins on histogram".format(
            which_bins
        )
