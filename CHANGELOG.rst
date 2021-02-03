MatPlotCheck Release Notes
==========================

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_, and this project adheres to
`Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

0.1.4
----------

-  Fixed issues with CI (@lwasser, #397)
-  Batch updated dependencies (@nkorinek, #398)

0.1.3
----------

-  Changed how `assert_lines` checks the limits of lines (@nkorinek, #243)
-  Changed changelog to an rst file. (@nkorinek, #266)
-  Add a vignette for testing vector data plots. (@nkorinek, #208)
-  Add ``pillow`` as a dev requirement (@lwasser, #253)
-  Removed the ``m2r`` package from MatPlotCheck (@nkorinek, #247)
-  Made ``assert_string_contains()`` accept a string instead of a list
   (@nkorinek, #53)
-  Added functions to get and assert the midpoint values of bins in a
   histogram (@nkorinek, #184)
-  Created tests for the autograde module (@nkorinek, #105)
-  Created tests for the vector module (@nkorinek, #209)
-  Created functions to test point geometries in VectorTester
   (@nkorinek, #176)
-  made ``assert_string_contains()`` accept correct strings with spaces
   in them (@nkorinek, #182)
-  added contributors file and updated README to remove that information
   (@nkorinek, #121)
-  Changed tolerance functionality from relative tolerance to absolute
   tolerance. (@ryla5068, #234)
-  Made checking line coverage optional for `base.assert_line()`
   (@ryla5068, #239)
-  Fixed bugs involving line tests (@ryla5068, #239)
-  Improved handling of datasets with different shapes in base.assert_xy() (@ryla5068, #233)
-  Bug fix for handling object datatypes in base.assert_xy() (@ryla5068, #232)

0.1.2
-----

-  Adding flake8 for format and other syntax issues! yay! (@lwasser,
   #195)
-  Created a vignette covering the testing of histograms (@ryla5068,
   #149)
-  Created ``get_plot_image()`` function for the RasterTester object
   (@nkorinek, #192)
-  Allowed ``assert_polygons()`` to accept GeoDataFrames and added tests
   (@nkorinek, #175)
-  raster test inherits from vector to allow for multi layer plot
   testing (@lwasser, #75)

0.1.1
-----

-  Added test for bin heights of histograms (@ryla5068, #124)
-  Added support for overlapping histograms in histogram tests
   (@ryla5068, #123)

0.1.0
-----

-  Created a vignette covering base plot tester functionality
   (@ryla5068, #122)
-  fix pip version to ensure pyproj installs in black tox envt
   (@lwasser, #144)
-  Changed ``get_caption()`` to return a string (@ryla5068, #125)
-  Updated ``assert_xlabel_ydata()`` to support pulling text from
   x-labels (@ryla5068, #125)
-  Fixed ``assert_xydata()`` incorrectly failing on some floating point
   numbers (@ryla5068, #124)
-  Updated all string content assertions in base to use the same syntax
   (@ryla5068, #132)
-  Moved tests for titles to ``test_base_titles.py`` (@ryla5068, #115)
-  Created ``test_base_data.py`` for data tests (@ryla5068, #114)
-  Added custom error messages to all assert functions in base module
   (@ryla5068, #106)
-  Added all missing docstrings to base module and updated existing ones
   (@ryla5068, #102)
-  Added significant test coverage to base module (@ryla5068, #101)
-  Replaced references to EarthPy in CONTRIBUTING.rst (@ryla5068, #100)
-  Add tests for raster module (@kysolvik, #32)
-  Added tests for base module – legend check methods (@kysolvik, #38)
-  Added tests for base modules – axis check methods (@kysolvik, #37)
-  Add conftest.py to centralize pytest fixtures (@kysolvik, #35)
-  Fix issue with pip 19.1 breaking appveyor build (@kysolvik, #46)
-  Fix Python version mismatch in pre-commit hook vs dev environment
   (@kysolvik, #31)
-  Adding cross platform builds to CI
