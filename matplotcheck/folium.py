import numpy as np
import folium


class FoliumTester(object):
    """object to test Folium plots

    Parameters
    ----------
    map: folium.folium.Map object

    """

    def __init__(self, fmap):
        """Initialize TestPlot object"""
        self.fmap = fmap

    def assert_map_type_folium(self):
        """Asserts fmap is of type folium.folium.Map"""
        assert type(self.fmap) == folium.folium.Map

    def assert_folium_marker_locs(
        self, markers, m="Markers not shown in appropriate location"
    ):
        """Asserts folium contains markers with locations described in markers_exp and only those markers, with error message m

        Parameters
        ----------
        markers: set of tuples where each tuple represents the x and y coord of an expected marker
        m: string error message if assertion is not met
        """
        marker_locs = set()
        while self.fmap._children:
            c = self.fmap._children.popitem()[1]
            if type(c) == folium.map.Marker:
                marker_locs.add(tuple(c.location))
        assert marker_locs == markers, m
