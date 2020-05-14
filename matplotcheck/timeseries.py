import numpy as np
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
import math

from .base import PlotTester


class TimeSeriesTester(PlotTester):
    """A PlotTester for 2 dimensional time series plots.

    Parameters
    ----------
    ax: ```matplotlib.axes.Axes``` object
        The plot to be tested.

    """

    def __init__(self, ax):
        """Initialize the time series tester"""
        super(TimeSeriesTester, self).__init__(ax)

    def assert_xticks_reformatted(
        self,
        tick_size="large",
        loc_exp=None,
        m="x ticks have not been reformatted properly",
    ):
        """Asserts that Axes ax xtick have been reformatted as denoted by
        tick_size and loc_exp, with error message m

        Parameters
        ----------
        tick_size: must be one of the following ['large','small']
            'large': if testing large ticks
            'small': if testing small ticks
        loc_exp: string ['decade','year', 'month', 'week', 'day']
            'decade': if tick should be shown every ten years
            'year': if tick should be shown every new year
            'month': if tick should be shown every new month
            'week': if tick should be shown every new week
            'day': if tick should be shown every new day
            None: if no tick format has been specified. This will automatically
            assert True
        m: string
            string error message if assertion is not met
        """
        if loc_exp:
            if tick_size == "large":
                test_date = (
                    self.ax.xaxis.get_major_formatter()
                    .format_data(735141)
                    .replace(" ", "")
                    .lower()
                )  # September 30, 2013
            elif tick_size == "small":
                test_date = (
                    self.ax.xaxis.get_minor_formatter()
                    .format_data(735141)
                    .replace(" ", "")
                    .lower()
                )  # September 30, 2013
            else:
                raise ValueError(
                    "tick_size must be on of the following string "
                    + "['large', 'small']"
                )
            if loc_exp == "decade" or loc_exp == "year":
                accepted_responses = ["2013"]
            elif loc_exp == "month":
                accepted_responses = ["sep", "september"]
            elif loc_exp == "week" or loc_exp == "day":
                accepted_responses = ["sep30", "september30"]
            else:
                raise ValueError(
                    """loc_exp must be one of the following strings ['decade',
                    'year', 'month', 'week', 'day', None]"""
                )
            assert test_date in accepted_responses, m

    def assert_xticks_locs(
        self,
        tick_size="large",
        loc_exp=None,
        m="Incorrect X axis tick locations",
    ):
        """Asserts that Axes ax has xaxis ticks as noted by tick_size and
        loc_exp

        Parameters
        ----------
        tick_size: str, opts: ['large','small']
            'large': if testing large ticks
            'small': if testing small ticks
        loc_exp: string ['decade','year', 'month', 'week', 'day']
            'decade': if tick should be shown every ten years
            'year': if tick should be shown every new year
            'month': if tick should be shown every new month
            'week': if tick should be shown every new week
            'day': if tick should be shown every new day
            None: if no tick location has been specified. This will
            automatically assert True
        m: error message if assertion is not met
        """

        if loc_exp:
            xlims = [mdates.num2date(limit) for limit in self.ax.get_xlim()]
            if tick_size == "large":
                ticks = self.ax.xaxis.get_majorticklocs()
            elif tick_size == "small":
                ticks = self.ax.xaxis.get_minorticklocs()
            else:
                raise ValueError(
                    """"Tick_size must be one of the following strings
                    ['large', 'small']"""
                )

            if loc_exp == "decade":
                inc = relativedelta(years=10)
            elif loc_exp == "year":
                inc = relativedelta(years=1)
            elif loc_exp == "month":
                inc = relativedelta(months=1)
            elif loc_exp == "week":
                inc = relativedelta(days=7)
            elif loc_exp == "day":
                inc = relativedelta(days=1)
            else:
                raise ValueError(
                    """"loc_exp must be one of the following strings ['decade',
                    'year', 'month', 'week', 'day'] or None"""
                )

            start, end = mdates.num2date(ticks[0]), mdates.num2date(ticks[-1])
            assert start < xlims[0] + inc, "Tick locators do not cover x axis"
            assert end > xlims[1] - inc, "Tick locators do not cover x axis"
            ticks_exp = [
                d.toordinal() for d in self._my_range(start, end, inc)
            ]
            np.testing.assert_equal(ticks, ticks_exp, m)

    def _my_range(self, start, end, step):
        """helper function for assert_xticks_locs
        alternative to range to use in a for loop. my_range allows for dataype
        other than ints. both start and end are included in the loop.

        Parameters
        ----------
        start: value to start while loop at
        end: last value to run in while loop
        step: about to increase between cycles in loop
              start, end, and step must be comparable datatypes.
        """
        while start <= end:
            yield start
            start += step

    def assert_no_data_value(self, nodata=999.99):
        """Asserts nodata values have been removed from the data, when x is a
        datetime with error message m

        Parameters
        ----------
        nodata: float or int
            a nodata value that will be searched for in dataset
        xtime: boolean
            does the x-axis contains datetime values?
        """
        if nodata:
            xy = self.get_xy(xtime=False)
            assert ~np.isin(nodata, xy["x"]), (
                "Values of {0} have been found in data. Be sure to remove no "
                "data values"
            ).format(nodata)
            assert ~np.isin(nodata, xy["y"]), (
                "Values of {0} have been found in data. Be sure to remove no "
                "data values"
            ).format(nodata)

    def assert_xdata_date(
        self, x_exp, m="X-axis is not in appropriate date format"
    ):
        """Asserts x-axis data has been parsed into datetime objects.
        Matplotlib changes datetime to floats representing number of days since
        day 0. If you are using dates prior to year 270, this assertion will
        fail.

        Parameters
        ----------
        x_exp: expected x_axis values, must be in a datetime format
        """
        x_data = [math.floor(d) for d in self.get_xy(xtime=False)["x"]]
        x_exp = [d.toordinal() for d in x_exp]  # convert to days elapsed
        assert np.array_equal(sorted(x_exp), sorted(x_data)), m
