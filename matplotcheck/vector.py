import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
import shapely

from .base import PlotTester


class VectorTester(PlotTester):
    """A PlotTester for spatial vector plots.

	Parameters
	----------
	ax: ```matplotlib.axes.Axes``` object

	"""

    def __init__(self, ax):
        """Initialize the vector tester"""
        super(VectorTester, self).__init__(ax)

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

    def _legends_overlap(self, b1, b2):
        """Helper function for assert_no_legend_overlap
		Boolean value if points of window extents for b1 and b2 overlap

		parmeters
		---------
		b1: bounding box of window extents
		b2: bounding box of window extents

		Returns
		------
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
                assert not self._legends_overlap(leg_extent1, leg_extent2), m

                ### VECTOR DATA FUNCTIONS ###
                ## MARKER POINTS ###

    def _convert_length(self, arr, n):
        """ helper function for 'get_points_by_attributes' and 'get_lines_by_attributes'
		takes an array of either legnth 1 or n. 
		If array is length 1: array of array's only element repeating n times is returned
		If array is length n: original array is returned
		Else: function raises value error

		Parameters
		----------
		arr: array of either length 1 or n
		n: length of return array

		Returns
		-------
		array of length n
		"""
        if len(arr) == 1:
            return list(arr) * n
        elif len(arr) == n:
            return arr
        else:
            raise ValueError(
                "Input array length is not of either expected values:1 or {0}".format(
                    n
                )
            )

    def get_points_by_attributes(self):
        """Returns a sorted list of lists where each list contains tuples of xycoords for points of 
		the same attributes: color, marker, and markersize

		Returns
		-------
		sorted list where each list represents all points with the same color.
		each point is represented by a tuple with its coordinates.
		"""
        points_dataframe = pd.DataFrame(
            columns=["offset", "color", "msize", "mstyle"]
        )
        for c in (
            coll
            for coll in self.ax.collections
            if type(coll) == matplotlib.collections.PathCollection
        ):
            colors, sizes = (
                [tuple(color) for color in c.get_facecolors()],
                c.get_sizes(),
            )
            styles, offsets = (
                [tuple(tuple(v) for v in p.vertices) for p in c.get_paths()],
                [tuple(o) for o in c.get_offsets()],
            )
            n = len(offsets)
            colors, sizes, styles = (
                self._convert_length(colors, n),
                self._convert_length(sizes, n),
                self._convert_length(styles, n),
            )
            points_dataframe = points_dataframe.append(
                pd.DataFrame(
                    {
                        "offset": offsets,
                        "color": colors,
                        "msize": sizes,
                        "mstyle": styles,
                    }
                ),
                ignore_index=True,
            )

        points_grouped = [
            [data["offset"][i] for i in data.index]
            for c, data in points_dataframe.groupby(
                ["color", "mstyle", "msize"], sort=False
            )
        ]
        return sorted([sorted(p) for p in points_grouped])

    def assert_points_grouped_by_type(
        self, data_exp, sort_column, m="Point attribtues not accurate by type"
    ):
        """Asserts that the points on Axes ax display attributes based on their type with error message m
		attributes tested are: color, marker, and markersize

		Parameters
		----------
		data_exp: Geopandas Dataframe with Point objects in column 'geometry'
			an additional column with title sort_column, denotes a category for each point
		sort_column: string of column label in dataframe data_exp.
			this column contains values expressing which points belong to which group
		m: string error message if assertion is not met
		"""

        groups = self.get_points_by_attributes()
        grouped_exp = [
            [(data.geometry[i].x, data.geometry[i].y) for i in data.index]
            for c, data in data_exp.groupby([sort_column], sort=False)
        ]
        np.testing.assert_equal(
            groups, sorted([sorted(p) for p in grouped_exp]), m
        )

    def sort_collection_by_markersize(self):
        """ Returns a pandas dataframe of points in collections on Axes ax.

		Returns
		--------
		pandas dataframe with columns x, y, point_size. Each row reprsents a point on Axes ax with location x,y and markersize pointsize
		"""
        df = pd.DataFrame(columns=("x", "y", "markersize"))
        for c in self.ax.collections:
            offsets, markersizes = c.get_offsets(), c.get_sizes()
            x_data, y_data = (
                [offset[0] for offset in offsets],
                [offset[1] for offset in offsets],
            )
            if len(markersizes) == 1:
                markersize = [markersizes[0]] * len(offsets)
                df2 = pd.DataFrame(
                    {"x": x_data, "y": y_data, "markersize": markersize}
                )
                df = df.append(df2)
            elif len(markersizes) == len(offsets):
                df2 = pd.DataFrame(
                    {"x": x_data, "y": y_data, "markersize": markersizes}
                )
                df = df.append(df2)
        df = df.sort_values(by="markersize").reset_index(drop=True)
        return df

    def assert_collection_sorted_by_markersize(self, df_expected, sort_column):
        """Asserts a collection of points vary in size by column expresse din sort_column

		Parameters
		----------
		df_expected: geopandas dataframe with geometry column of expected point locations
		sort_column: column title from df_expected that points are expected to be sorted by
			if None, assertion is passed
		"""
        df = self.sort_collection_by_markersize()
        df_expected = df_expected.sort_values(by=sort_column).reset_index(
            drop=True
        )
        np.testing.assert_almost_equal(
            np.array(df.x),
            np.array([p.x for p in df_expected.geometry]),
            decimal=6,
            err_msg="Markersize not based on {0} values".format(sort_column),
        )
        np.testing.assert_almost_equal(
            np.array(df.y),
            np.array([p.y for p in df_expected.geometry]),
            decimal=6,
            err_msg="Markersize not based on {0} values".format(sort_column),
        )

        ### LINES ###

    def _convert_multilines(self, df, column_title):
        """Helper function for get_lines_by_attribute
		converts a pandas dataframe containing a column of LineString and MultiLinestring objects
		to a pandas dataframe where each row represents a single line. Line segment values are converted
		to a list of tuples.

		Parameters
		---------
		df: pandas Dataframe containing a column of LineString and MultiLinestring objects
		column_title: string of column title which holds LineString and MultLinestring objects

		Returns
		-------
		Dataframe where each row repsrents a single line.
		Line segments values are converted to a list of tuples in column column_title
		"""
        dfout = df.copy()
        for i, row in dfout.iterrows():
            seg = row[column_title]
            if type(seg) == shapely.geometry.linestring.LineString:
                dfout.at[i, column_title] = list(seg.coords)
            elif type(seg) == shapely.geometry.multilinestring.MultiLineString:
                dfout.at[i, column_title] = list(seg[0].coords)
                for j in range(1, len(seg)):
                    new_row = row.copy()
                    new_row[column_title] = list(seg[j].coords)
                    dfout = dfout.append(new_row).reset_index(drop=True)
            else:
                raise ValueError(
                    "Segment is not of either expected type: MultiLinestring, LineString"
                )
        return dfout

    def _convert_linestyle(self, ls):
        """helper function for get_lines_by_attributes.
			converts linestyle to a tuple of (offset, onoffseq) to get hashable datatypes

		Parameters
		----------
		ls: linesytle from a LineCollection retreived by get_linestyle()

		Returns
		-------
		tuple containing (offset, onoffseq) of linestyle
		"""
        onoffseq = ls[1]
        if onoffseq:
            onoffseq = tuple(ls[1])
        return (ls[0], onoffseq)

    def get_lines(self):
        """Returns a dataframe with all lines on ax 

		Returns
		-------
		output: DataFrame with column 'lines'. Each row represents one line segment. 
		Its value in 'lines' is a list of tuples representing the line segement.
		"""
        lines = [
            [tuple(coords) for coords in seg]
            for c in self.ax.collections
            if type(c) == matplotlib.collections.LineCollection
            for seg in c.get_segments()
        ]
        return pd.DataFrame({"lines": lines})

    def get_lines_by_collection(self):
        """Returns a sorted list of list where each list contains line segments from the same collections

		Returns
		-------
		sorted list where each list represents all lines from the same collection
		"""
        lines_grouped = [
            [[tuple(coords) for coords in seg] for seg in c.get_segments()]
            for c in self.ax.collections
            if type(c) == matplotlib.collections.LineCollection
        ]
        return sorted([sorted(l) for l in lines_grouped])

    def get_lines_by_attributes(self):
        """Returns a sorted list of lists where each list contains line segments of the same attributes:
			color, linewidth, and linestyle

		Returns
		------
		sorted list where each list represents all lines with the same attributes
		"""
        lines_dataframe = pd.DataFrame(
            columns=["seg", "color", "lwidth", "lstyle"]
        )
        for c in (
            coll
            for coll in self.ax.collections
            if type(coll) == matplotlib.collections.LineCollection
        ):
            segs = [[tuple(coords) for coords in s] for s in c.get_segments()]
            colors, widths, styles = (
                [tuple(color) for color in c.get_colors()],
                c.get_linewidth(),
                [self._convert_linestyle(ls) for ls in c.get_linestyle()],
            )
            n = len(segs)
            colors, widths, styles = (
                self._convert_length(colors, n),
                self._convert_length(widths, n),
                self._convert_length(styles, n),
            )
            lines_dataframe = lines_dataframe.append(
                pd.DataFrame(
                    {
                        "seg": segs,
                        "color": colors,
                        "lwidth": widths,
                        "lstyle": styles,
                    }
                ),
                ignore_index=True,
            )

        lines_grouped = [
            [data["seg"][i] for i in data.index]
            for c, data in lines_dataframe.groupby(
                ["color", "lwidth", "lstyle"], sort=False
            )
        ]
        return sorted([sorted(l) for l in lines_grouped])

    def assert_lines(self, lines_expected, m="Incorrect Line Data"):
        """Asserts the line data in Axes ax is equal to lines_expected with error message m.
		If line_expected is None or an empty list, assertion is passed

		Parameters
		----------
		lines_expected: Geopandas Dataframe with a geometry column consisting of MultilineString and LineString objects
		m: string error message if assertion is not met
		"""
        if type(lines_expected) == gpd.geodataframe.GeoDataFrame:
            lines_expected = lines_expected[
                lines_expected["geometry"].is_empty == False
            ].reset_index(drop=True)
            fig, ax_exp = plt.subplots()
            lines_expected.plot(ax=ax_exp)
            lines_exp = VectorTester(ax=ax_exp).get_lines()
            plt.close(fig)
            np.testing.assert_equal(
                sorted(self.get_lines().lines), sorted(lines_exp.lines), m
            )
        elif not lines_expected:
            pass
        else:
            raise ValueError(
                "lines_expected is not expected type: GeoDataFrame"
            )

    def assert_lines_grouped_by_type(
        self,
        lines_expected,
        sort_column,
        m="Line attributes not accurate by type",
    ):
        """Asserts that the lines on Axes ax display like attributes based on their type with error message m
		attributes tested are: color, linewidth, linestyle

		Parameters
		----------
		lines_expected: Geopandas Dataframe with geometry column consisting of MultiLineString and LineString objects
		sort_column: string of column title in lines_expected that contains types lines are expected to be grouped by
		m: string error message if assertion is not met
		"""
        if type(lines_expected) == gpd.geodataframe.GeoDataFrame:
            groups = self.get_lines_by_attributes()
            lines_expected = lines_expected[
                lines_expected["geometry"].is_empty == False
            ].reset_index(drop=True)
            fig, ax_exp = plt.subplots()
            for typ, data in lines_expected.groupby(sort_column):
                data.plot(ax=ax_exp)
            grouped_exp = [
                [[tuple(coords) for coords in seg] for seg in c.get_segments()]
                for c in ax_exp.collections
                if type(c) == matplotlib.collections.LineCollection
            ]
            grouped_exp = sorted([sorted(l) for l in grouped_exp])
            plt.close(fig)
            np.testing.assert_equal(groups, grouped_exp, m)
        elif not lines_expected:
            pass
        else:
            raise ValueError(
                "lines_expected is not of expected type: GeoDataFrame"
            )

            ### POLYGONS ###

    def get_polygons(self):
        """Returns all polygons on Axes ax as a sorted list of polygons where each polygon is a list of coord tuples

		Returns
		-------
		output: sorted list of polygons. Each polygon is a list tuples. Ecah tuples is a coordinate.
		"""
        output = [
            [tuple(coords) for coords in path.vertices]
            for c in self.ax.collections
            if type(c) == matplotlib.collections.PatchCollection
            for path in c.get_paths()
        ]
        return sorted(output)

    def _convert_multipolygons(self, series):
        """Helper function for assert_polygons
		converts a pandas series of Polygon and MultiPolygon objects to a list of lines,
		where each line is a list of coord tuples for the exterior

		Parameters
		----------
		series: series where each entry is a Polygon or MultiPolygon

		Returns
		-------
		list of lines where each line is a list of coord tuples for the exterior polygon
		"""
        output = []
        for entry in series:
            if type(entry) == shapely.geometry.multipolygon.MultiPolygon:
                for poly in entry:
                    output += [list(poly.exterior.coords)]
            if type(entry) == shapely.geometry.polygon.Polygon:
                output += [list(entry.exterior.coords)]
        return output

    def assert_polygons(
        self, polygons_expected, dec=None, m="Incorrect Polygon Data"
    ):
        """Asserts the polygon data in Axes ax is equal to polygons_expected to decimal place dec with error message m
		If polygons_expected is am empty list or None, assertion is passed
		
		Parameters
		----------
		polygons_expected: list of polygons expected to be founds on Axes ax
		dec: int stating the desired decimal precision. If None, polygons must be exact
		m: string error message if assertion is not met
		"""
        if polygons_expected:
            polygons = self.get_polygons()
            if dec:
                assert len(polygons_expected) == len(polygons), m
                polygons_expected = sorted(polygons_expected)
                for i in range(len(polygons)):
                    np.testing.assert_almost_equal(
                        polygons[i],
                        polygons_expected[i],
                        decimal=dec,
                        err_msg=m,
                    )
            else:
                np.testing.assert_equal(polygons, sorted(polygons_expected), m)
