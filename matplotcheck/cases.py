import unittest
from .base import PlotTester
from .timeseries import TimeSeriesTester
from .vector import VectorTester
from .raster import RasterTester
from .folium import FoliumTester


def loadTests(tests):
    loader = unittest.TestLoader()
    suites = []
    for test in tests:
        suite = loader.loadTestsFromTestCase(test)
        suites.append(suite)
    test_suite = unittest.TestSuite(suites)
    return test_suite


class PlotBasicSuite(object):
    """A generic object to test a basic 2d Matplotlib plot (scatter, bar, line)

    Parameters
    ----------
    ax: Matplotlib Axes to be tested
    data_exp: pandas dataframe containing plot data
    xcol: string column title in data_exp that contains xaxis data
    ycol: string column title in data_exp that contains yaxis data
    plot_type: string from list ["scatter","bar"] of expected plot type
    line_types: list of strings. Acceptable strings in line_types are as
        follows ["regression", "onetoone"]. If list is empty, assert is passed
    xlabels: boolean if using x axis labels rather than x data
    lims_equal: boolean expressing if x and y limits are expected to be equal
    title_contains: list of lower case strings where each string is expected to
    be in title, barring capitalization.
        If value is an empty list: test is just to see that title exists and is
        not an empty string
        If value is None: no tests are run
    title_type: one of the following strings ["figure", "axes", "either"]
        "figure": only the figure title (suptitle) will be tested
        "axes": only the axes title (suptitle) will be tested
        "either": either the figure title or axes title will pass this
        assertion.
        The combined title will be tested.
    xlabel_contains: list of lower case strings where each string is expected
    to be in x-axis label, barring capitalization.
        If value is an empty list: test is just to see that x-axis label exists
        and is not an empty string
        If value is None: no tests are run
    ylabel_contains: list of lower case strings where each string is expected
    to be in y-axis label, barring capitalization.
        If value is an empty list: test is just to see that y-axis label exists
        and is not an empty string
        If value is None: no tests are run
    caption_string: list of lists. Each internal list is a list of lower case
    strings where at least one string must be
        found in the caption, barring capitalization
        if empty list: asserts caption exists and not an empty string
        if None: no tests are run
    legend_labels: list of lower case stings. Each string is an expected entry
    label in the legend, barring capitalization.
    """

    def __init__(
        self,
        ax,
        data_exp=None,
        xcol=None,
        ycol=None,
        plot_type=None,
        line_types=None,
        xlabels=False,
        lims_equal=False,
        title_contains=[],
        title_type="either",
        xlabel_contains=[],
        ylabel_contains=[],
        caption_strings=[],
        legend_labels=None,
        title_points=1,
        xlab_points=1,
        ylab_points=1,
    ):
        class PlotLabelsTest(unittest.TestCase):
            """A unittest.TestCase containing 3 tests:
            1. title_exist: ax has a title that contains each string in list of
            strings title_contains, barring capitalization
            2. xlab_exist: ax has a x label that contains each string in list
            of strings xlabel_contains, barring capitalization
            3. ylab_exist: ax has a y label that that contains each string in
            list of strings ylabel_contains, barring capitalization
            """

            def setUp(self):
                self.pt = PlotTester(ax)

            @unittest.skipIf(title_contains is None, "Skip title test")
            def test_title_exist(self):
                self.pt.assert_title_contains(
                    lst=title_contains, title_type=title_type
                )

            @unittest.skipIf(xlabel_contains is None, "Skip x axis label test")
            def test_xlab_exist(self):
                self.pt.assert_axis_label_contains(
                    axis="x", lst=xlabel_contains
                )

            @unittest.skipIf(ylabel_contains is None, "Skip y axis label test")
            def test_ylab_exist(self):
                self.pt.assert_axis_label_contains(
                    axis="y", lst=ylabel_contains
                )

            def tearDown(self):
                self.pt = None

        class LegendTest(unittest.TestCase):
            """A unittest.TestCase containing 2 tests checking the legend(s):
            1. legend_labels: Asserts the legend has labels specified in
            labels_ exp (barring capitalization), and only those labels
            2. legend_location: Asserts legend does not cover data and no
            legends overlap each other
            """

            def setUp(self):
                self.pt = PlotTester(ax)

            @unittest.skipIf(legend_labels is None, "Skip legend test")
            def test_legend_labels(self):
                self.pt.assert_legend_labels(labels_exp=legend_labels)

            @unittest.skipIf(legend_labels is None, "Skip legend test")
            def test_legend_location(self):
                self.pt.assert_no_legend_overlap()
                self.pt.assert_legend_no_overlay_content()

            def tearDown(self):
                self.pt = None

        class PlotCaption(unittest.TestCase):
            """Returns a unittest.TestCase containing 1 test for an
            appropriate caption:

            Test 1 - caption_words: caption contains one string from each of
            the list of strings in strings_exp, barring capitalization.
            """

            def setUp(self):
                self.pt = PlotTester(ax)

            @unittest.skipIf(caption_strings is None, "Skip caption test")
            def test_caption_words(self):
                self.pt.assert_caption_contains(strings_exp=caption_strings)

            def tearDown(self):
                self.pt = None

        class PlotBasic(unittest.TestCase):
            """A unittest.TestCase containing 4 tests on Matplotlib Axes ax
            1. data: asserts that the x and y data of ax matches data_exp
            2. lines: asserts each of lines in line_types is displayed on ax
            3. plot_type: asserts plot is of expected type expressed by
            plot_type
            4. lims: asserts the x and y limits are equal if boolean
            lims_equal expresses it should be
            """

            def setUp(self):
                self.pt = PlotTester(ax)

            @unittest.skipIf(data_exp is None, "Skip data test")
            def test_data(self):
                points_only = False
                if plot_type == "scatter":
                    points_only = True
                self.pt.assert_xydata(
                    xy_expected=data_exp,
                    xcol=xcol,
                    ycol=ycol,
                    points_only=points_only,
                    xtime=False,
                    xlabels=xlabels,
                )

            @unittest.skipIf(
                line_types is None, "No additional lines requested"
            )
            def test_lines(self):
                self.pt.assert_lines_of_type(line_types=line_types)

            @unittest.skipIf(
                plot_type is None, "No specific plot type requested"
            )
            def test_plot_type(self):
                self.pt.assert_plot_type(plot_type=plot_type)

            @unittest.skipIf(not lims_equal, "Limits do not need to be equal")
            def test_lims(self):
                self.pt.assert_equal_xlims_ylims()

            def tearDown(self):
                self.pt = None

        self.LabelsCase = PlotLabelsTest
        self.CaptionCase = PlotCaption
        self.LegendCase = LegendTest
        self.BasicCase = PlotBasic

    @property
    def cases(self):
        """Returns a list of TestCases to be run in a TestLoader for basic 2d
        plots (scatter, bar, line, etc.).

        Testcases are as follows:
        1. LabelsCase: Asserts the title, x-axis label, and y-axis label are
        as expected
        2. BasicCase: Asserts data matches data_exp, and other assertions
        based on params listed below
        For more on tests, see init method above. For more on assertions,
        see the autograde package.
        """
        return [self.LabelsCase, self.BasicCase]

    @property
    def suite(self):
        """Returns a Testsuite from cases to be run in a TestRunner"""
        return loadTests(self.cases)


""" HISTOGRAM """


class PlotHistogramSuite(PlotBasicSuite):
    """A PlotBasicSuite object to test a Matplotlib histogram plot.
    Since students have the flexibility to determine bin size, we are testing
    the set up of the
    histogram more than the data in the histogram itself.

    Parameters
    ----------
    ax: Matplotlib Axes to be tested
    n_bins: tuple of ints. First int is the minimum number of bins containing
        negative values.
        Second int is the minimum number of bins containing positive values
    xlims: tuple of 2 tuples. First tuple contains range the left x limit must
        be in, exclusive.
        Second tuple contains range the right x limit must be in, exclusive.
    ylims: tuple of 2 tuples. First tuple contains range the bottom y limit
        must be in, exclusive.
        Second tuple contains range the top y limit must be in, exclusive.
    title_contains: list of lower case strings where each string is expected to
        be in title, barring capitalization.
        If value is an empty list: test is just to see that title exists and is
        not an empty string
        If value is None: asserts no title
    xlabel_contains: list of lower case strings where each string is expected
        to be in x-axis label, barring capitalization.
        If value is an empty list: test is just to see that x-axis label exists
        and is not an empty string
        If value is None: asserts no label is expressed
    ylabel_contains: list of lower case strings where each string is expected
        to be in y-axis label, barring capitalization.
        If value is an empty list: test is just to see that y-axis label exists
        and is not an empty string
        If value is None: asserts no label is expressed
    """

    def __init__(
        self,
        ax,
        n_bins=None,
        xlims=None,
        ylims=None,
        title_contains=[],
        xlabel_contains=[],
        ylabel_contains=[],
    ):
        """Initialize PlotHisogramSuite object"""
        super(PlotHistogramSuite, self).__init__(
            ax,
            title_contains=title_contains,
            xlabel_contains=xlabel_contains,
            ylabel_contains=ylabel_contains,
        )

        class PlotHistogram(unittest.TestCase):
            """A unittest.TestCase containing 4 tests for a histogram:
            Test 1 - num_neg_bins: number of bins centered at a negative
            value is greater than n_bins[0]
            Test 2- num_pos_bins: number of bins centered at a positive value
            is greater than n_bins[1]
            Test 3 - x-lims: x-axis left limits are within the bounds [xlims[
            0][0], xlims[0][1]] and
            x-axis right limits are within the bounds [xlims[1][0],
            xlims[1][1]]
            Test 4 -  y_lims: y-axis bottom limits are within the bounds [
            ylims[0][0], ylims[0][1]] and
            y-axis top limits are within the bounds [ylims[1][0], ylims[1][1]]
            """

            def setUp(self):
                self.pt = PlotTester(ax)

            @unittest.skipIf(
                n_bins is None, "No specified number of bins required"
            )
            def test_num_neg_bins(self):
                self.pt.assert_num_bins(n=n_bins[0], which_bins="negative")

            @unittest.skipIf(
                n_bins is None, "No specified number of bins required"
            )
            def test_num_pos_bins(self):
                self.pt.assert_num_bins(n=n_bins[1], which_bins="positive")

            @unittest.skipIf(xlims is None, "No specified x limits")
            def test_x_lims(self):
                self.pt.assert_lims_range(lims_range=xlims, axis="x")

            @unittest.skipIf(ylims is None, "No specified y limits")
            def test_y_lims(self):
                self.pt.assert_lims_range(lims_range=ylims, axis="y")

            def tearDown(self):
                self.pt = None

        self.HistogramCase = PlotHistogram

    @property
    def cases(self):
        """Returns list of cases for a histogram. Testcases are as follows:
        1. LabelsCase: Asserts the title, x-axis label, and y-axis label are
        as expected
        2. HistogramCase: number of negative and positive bins as declares in
        n_bins. x axis limits and y axis limits
        are in range declared by xlims and y lims.
        For more on tests, see init method above. For more on assertions,
        see the autograde package.
        """
        return [self.LabelsCase, self.HistogramCase]


""" TIME SERIES PLOTS """


class PlotTimeSeriesSuite(PlotBasicSuite):
    """A PlotBasicSuite object to test Matplotlib time series plots.

    Parameters
    ----------
    ax: Matplotlib Axes to be tested
    data_exp: pandas dataframe containing plot data
    x_col: string column title in data_exp that contains xaxis data
    y_col: string column title in data_exp that contains yaxis data
    no_data_val: float representing no data, as stated by the input data
    major_locator_exp: one of the following ['decade', 'year', 'month',
    'week', 'day', None]
        decade: if tick should be shown every ten years
        year: if tick should be shown every new year
        month: if tick should be shown every new month
        week: if tick should be shown every new week
        day: if tick should be shown every new day
    minor_locator_exp: one of the following ['decade', 'year', 'month',
    'week', 'day', None], as expressed above
    title_contains: list of lower case strings where each string is expected
    to be in title, barring capitalization.
        If value is an empty list: test is just to see that title exists and
        is not an empty string
        If value is None: asserts no title
    xlabel_contains: list of lower case strings where each string is expected
    to be in x-axis label, barring capitalization.
        If value is an empty list: test is just to see that x-axis label
        exists and is not an empty string
        If value is None: asserts no label is expressed
    ylabel_contains: list of lower case strings where each string is expected
    to be in y-axis label, barring capitalization.
        If value is an empty list: test is just to see that y-axis label
        exists and is not an empty string
        If value is None: asserts no label is expressed
    """

    def __init__(
        self,
        ax,
        data_exp,
        xcol,
        ycol,
        no_data_val=None,
        major_locator_exp=None,
        minor_locator_exp=None,
        title_contains=[],
        xlabel_contains=[],
        ylabel_contains=[],
    ):
        """Initialize PlotTimeSeriesSuite object"""
        super(PlotTimeSeriesSuite, self).__init__(
            ax=ax,
            data_exp=data_exp,
            xcol=xcol,
            ycol=ycol,
            title_contains=title_contains,
            xlabel_contains=xlabel_contains,
            ylabel_contains=ylabel_contains,
        )

        class PlotTicksReformat(unittest.TestCase):
            """A unittest.TestCase containing 3 tests checking the xaxis
            ticks and labels:
            1. x_major_formatter: large ticks on x axis have been reformatted
            as expressed in major_locator_exp
            2. x_major_locs: large ticks on x axis are located as expressed
            in major_locator_exp
            3. x_minor_locs: small ticks on x axis are located as expressed
            in minor_locator_exp
            """

            def setUp(self):
                self.tst = TimeSeriesTester(ax)

            @unittest.skipIf(
                major_locator_exp is None, "No expected large tick format"
            )
            def test_x_major_formatter(self):
                self.tst.assert_xticks_reformatted(
                    tick_size="large", loc_exp=major_locator_exp
                )

            @unittest.skipIf(
                major_locator_exp is None, "No expected large tick locator"
            )
            def test_x_major_locs(self):
                self.tst.assert_xticks_locs(
                    tick_size="large", loc_exp=major_locator_exp
                )

            @unittest.skipIf(
                minor_locator_exp is None, "No expected small tick locator"
            )
            def test_x_minor_locs(self):
                self.tst.assert_xticks_locs(
                    tick_size="small", loc_exp=minor_locator_exp
                )

            def tearDown(self):
                self.tst = None

        class PlotTimeSeries(unittest.TestCase):
            """A unittest.TestCase containing 3 tests for time series plots.

            yna_vals: y data on ax does not contain no_data_val
            x_datetime: values on x-axis are datetime
            xy_data: x and y data on ax is as expected according to data_exp
            """

            def setUp(self):
                self.tst = TimeSeriesTester(ax)

            @unittest.skipIf(
                no_data_val is None, "No data value not specified"
            )
            def test_yna_vals(self):
                self.tst.assert_no_data_value(nodata=no_data_val)

            def test_x_datetime(self):
                self.tst.assert_xdata_date(x_exp=data_exp[xcol])

            def test_xydata(self):
                self.tst.assert_xydata(
                    xy_expected=data_exp, xcol=xcol, ycol=ycol, xtime=True
                )

            def tearDown(self):
                self.tst = None

        self.TickReformatCase = PlotTicksReformat
        self.TimeSeriesCase = PlotTimeSeries

    @property
    def cases(self):
        """Returns a list of TestCases for time series plots.
        Testcase are as follows:
        1. LabelsCase: Asserts the title, x-axis label, and y-axis label are
        as expected
        2. TickReformatCase: Asserts x-axis ticks have large ticks as express
        in major_locator_exp and small
        ticks as express in minor_locator_exp
        3. TimeSeriesCase: Asserts data matches data_exp and is converted to
        time objects
        For more on tests, see init method above. For more on assertions,
        see the autograde package.
        """
        return [self.LabelsCase, self.TickReformatCase, self.TimeSeriesCase]


""" VECTOR PLOTS """


class PlotVectorSuite(PlotBasicSuite):
    """A PlotBasicSuite object to test a Matplotlib plot with spatial vector
    data.

    Parameters
    ---------
    ax: Matplotlib Axes to be tested
    caption_strings: list of lists. Each internal list is a list of lower
    case strings where at least one string must be
        found in the caption, barring capitalization
        if None: assert caption does not exist
        if empty list: asserts caption exists and not an empty string
    legend_labels: list of lower case stings. Each string is an expected
    entry label in the legend.
    title_type: one of the following strings ["figure", "axes", "either"]
        "figure": only the figure title (suptitle) will be tested
        "axes": only the axes title (suptitle) will be tested
        "either": either the figure title or axes title will pass this
        assertion.
        The combined title will be tested.
    title_contains: list of lower case strings where each string is expected
    to be in title, barring capitalization.
        If value is an empty list: test is just to see that title exists and
        is not an empty string
        If value is None: asserts no title
    markers: Geopandas dataframe with geometry column containing expected
    Point objects
    lines: Geopandas dataframe with geometry column containing expected
    LineString and MultiLineString objects
    polygons: list of lines where each line is a list of coord tuples for the
    exterior polygon
    markers_groupby: column title from markers_exp that points are expected
    to be grouped by/contain
        like attributes. Attributes tested are: marker type, markersize,
        and color
        if None, assertion is passed
    lines_groupby: column title from line_exp that lines are expected to be
    grouped by/contain
        like attributes. Attributes tested are: line style, line width,
        and color
        if None, assertion is passed
    markers_by_size: column title from markers_exp that points are expected
    to be sorted by
        if None, assertion is passed
    """

    def __init__(
        self,
        ax,
        caption_strings,
        legend_labels,
        title_type="either",
        title_contains=[],
        markers=None,
        lines=None,
        polygons=None,
        markers_groupby=None,
        lines_groupby=None,
        markers_by_size=None,
    ):
        """Initialize PlotVectorSuite object"""
        super(PlotVectorSuite, self).__init__(
            ax=ax,
            caption_strings=caption_strings,
            legend_labels=legend_labels,
            title_type=title_type,
            title_contains=title_contains,
            xlabel_contains=None,
            ylabel_contains=None,
        )

        class PlotVector(unittest.TestCase):
            """A unittest.TestCase containing tests for a spatial vector plot.
            1. marker_location: points on ax match markers
            2. markers_by_size: asserts points on ax vary in size by column
            expressed in markers_by_size
            3. markers_grouped: asserts markers of the same group contain
            like attributes
            4. lines_location: lines on ax match lines
            5. lines_grouped: asserts lines of the same group contain like
            attributes
            6. polygons_location: polygons on ax match polygons
            """

            def setUp(self):
                self.vt = VectorTester(ax)

            @unittest.skipIf(markers is None, "No expected markers")
            def test_marker_location(self):
                self.vt.assert_xydata(
                    xy_expected=markers,
                    points_only=True,
                    m="Incorrect marker locations",
                )

            @unittest.skipIf(
                markers_by_size is None, "No markersize variation required"
            )
            def test_markers_by_size(self):
                self.vt.assert_collection_sorted_by_markersize(
                    df_expected=markers, sort_column=markers_by_size
                )

            @unittest.skipIf(
                markers_groupby is None, "No expected marker groupby"
            )
            def test_markers_grouped(self):
                if markers_groupby:
                    self.vt.assert_points_grouped_by_type(
                        data_exp=markers, sort_column=markers_groupby
                    )

            @unittest.skipIf(lines is None, "No expected lines")
            def test_lines_location(self):
                self.vt.assert_lines(lines_expected=lines)

            @unittest.skipIf(
                lines_groupby is None, "No expected lines groupby"
            )
            def test_lines_grouped(self):
                if lines_groupby:
                    self.vt.assert_lines_grouped_by_type(
                        lines_expected=lines, sort_column=lines_groupby
                    )

            @unittest.skipIf(polygons is None, "No expected polygons")
            def test_polygons_location(self):
                self.vt.assert_polygons(polygons_expected=polygons, dec=4)

            def tearDown(self):
                self.vt = None

        self.VectorCase = PlotVector

    @property
    def cases(self):
        """Returns a list of TestCases for spatial vector plots.
        Testcase are as follows:
        1. CaptionCase: assert caption is in appropriate location with
        strings expressed in caption_contains
        2. LabelsCase: asserts the title contains strings in title_contains,
        and x and y labels are empty
        3. LegendCase: assert legend(s) is/are in appropriate location with
        legend_labels
        4. VectorCase: assert vector data is as expected in markers, lines,
        and polygons
        For more on tests, see init method above. For more on assertions,
        see the autograde package.
        """
        return [
            self.CaptionCase,
            self.LabelsCase,
            self.LegendCase,
            self.VectorCase,
        ]


""" RASTER PLOT """


class PlotRasterSuite(PlotVectorSuite):
    """A PlotBasicSuite object to test a Matplotlib raster plot.

    Parameters
    ---------
    ax: Matplotlib Axes to be tested
    im_expected: array containing values of an expected image
    caption_strings: list of lists. Each internal list is a list of strings
    where at least one string must be
        found in the caption, barring capitalization
        if empty list: asserts caption exists and not an empty string
        if None: assertion is passed
    im_classified: boolean if image on ax is classfied
    legend_labels: list of lists. Each internal list represents a
    classification category.
        Said list is a list of strings where at least one string is expected
        to be in the legend label for this category.
        Internal lists must be in the same order as bins in im_expected.
    title_type: one of the following strings ["figure", "axes", "either"],
    stating which title to test
    title_contains: list of strings expected to be in title
    markers: Geopandas dataframe with geometry column containing expected
    Point objects
    markers_by_size: column title from markers_exp that points are expected
    to be sorted by
        if None, assertion is passed
    markers_groupby: column title from markers_exp that points are expected
    to be grouped by/contain
        like attributes. Attributes tested are: marker type, markersize,
        and color
        if None, assertion is passed
    lines: Geopandas dataframe with geometry column containing expected
    LineString and MultiLineString objects
    lines_groupby: column title from line_exp that lines are expected to be
    grouped by/contain
        like attributes. Attributes tested are: line style, line width,
        and color
        if None, assertion is passed
    polygons: list of lines where each line is a list of coord tuples for the
    exterior polygon
    colorbar_range: tuple of (min, max) for colorbar.
        If empty tuple: asserts a colorbar exists, but does not check values
        If None: assertion is passed
    """

    def __init__(
        self,
        ax,
        im_expected,
        caption_strings,
        im_classified=True,
        legend_labels=None,
        title_type="either",
        title_contains=[],
        markers=None,
        markers_by_size=None,
        markers_groupby=None,
        lines=None,
        lines_groupby=None,
        polygons=None,
        colorbar_range=None,
    ):
        """Initialize PlotRasterSuite object"""
        super(PlotRasterSuite, self).__init__(
            ax=ax,
            caption_strings=caption_strings,
            legend_labels=legend_labels,
            markers=markers,
            markers_by_size=markers_by_size,
            markers_groupby=markers_groupby,
            lines=lines,
            lines_groupby=lines_groupby,
            polygons=polygons,
            title_type=title_type,
            title_contains=title_contains,
        )

        class PlotRaster(unittest.TestCase):
            """A unittest.TestCase containing tests for a spatial raster plot.
            1. image_data: asserts image is as expected. If Image is
            classified image classification may be shifted or reversed.
            2. image_stretch: asserts image takes up entire display as expected
            3. image_mask:
            4. legend_accuracy: if image is classified, asserts legend exists
            and correctly describes image.
                if image is not classified, assertion is passed.
            5. colorbar_accuracy: asserts colorbar exists and has range
            descrbied in colorbar_range
            6. axis_off: axis lines are not displayed
            """

            def setUp(self):
                self.rt = RasterTester(ax)

            @unittest.skipIf(im_expected is None, "No expected image")
            def test_image_data(self):
                self.rt.assert_image(
                    im_expected=im_expected, im_classified=im_classified
                )

            @unittest.skipIf(im_expected is None, "No expected image")
            def test_image_stretch(self):
                self.rt.assert_image_full_screen()

            @unittest.skip("Mask test not implemented")
            def test_image_mask(self):
                pass

            @unittest.skipIf(
                not im_classified, "Image not expected to be classified"
            )
            def test_legend_accuracy(self):
                self.rt.assert_legend_accuracy_classified_image(
                    im_expected=im_expected, all_label_options=legend_labels
                )

            @unittest.skipIf(colorbar_range is None, "No expected colorbar")
            def test_colorbar_accuracy(self):
                self.rt.assert_colorbar_range(crange=colorbar_range)

            def test_axis_off(self):
                self.rt.assert_axis_off()

            def tearDown(self):
                self.rt = None

        self.RasterCase = PlotRaster

    @property
    def cases(self):
        """Returns a list of TestCases for spatial raster plots.
        Testcase are as follows:
        1. CaptionCase: assert caption is in appropriate location with
        strings expressed in caption_strings
        2. LabelsCase: asserts the title contains strings in title_contains,
        and x and y labels are empty
        3. RasterCase: asserts raster image matches im_expected and legend is
        correct if image is classified
        4. VectorCase: assert vector data is as expected
        """
        return [
            self.CaptionCase,
            self.LabelsCase,
            self.RasterCase,
            self.VectorCase,
        ]


""" FOLIUM """


class PlotFoliumSuite(object):
    """A generic object to test Folium Maps.

    Parameters
    ---------
    fmap: folium map to be tested
    markers: set of tuples where each tuple represents the x and y coord of
    an expected marker
    """

    def __init__(self, fmap, markers):
        class MapFolium(unittest.TestCase):
            """Returns a unittest.TestCase containing 2 tests on a Folium map.
            1. map_folium: map is of type folium.folium.Map
            2. marker_locs: map contains all markers in markers_exp and no
            additional markers
            """

            def setUp(self):
                self.ft = FoliumTester(fmap)

            def test_map_folium(self):
                self.ft.assert_map_type_folium()

            @unittest.skipIf(markers is None, "No markers searched for")
            def test_marker_locs(self):
                self.ft.assert_folium_marker_locs(markers=markers)

            def tearDown(self):
                self.ft = None

        self.FoliumCase = MapFolium

    @property
    def cases(self):
        """Returns a TestSuite for Folium Maps.
        Testcase are as follows:
        1. FoliumCase: asserts map is of type folium.map and contains
        expected markers
        """
        return [self.FoliumCase]

    @property
    def suite(self):
        """ Returns a Testsuite from cases to be run in a TestRunner"""
        return loadTests(self.cases)
