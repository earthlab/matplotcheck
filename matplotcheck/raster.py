import numpy as np
from .vector import VectorTester


class RasterTester(VectorTester):
    """A PlotTester for spatial raster plots.

    Parameters
    ----------
    ax: ```matplotlib.axes.Axes``` object

    """

    def __init__(self, ax):
        """Initialize the raster tester"""
        super(RasterTester, self).__init__(ax)

    def get_colorbars(self):
        """Retrieve list of colorbars on axes ax

        Returns
        ----------
        list of matplotlib.colorbar.Colorbar objects on axes.
            If no colorbars exist, Returns an empty list.
        """
        cb = [im.colorbar for im in self.ax.images if im.colorbar]
        return cb

    def assert_colorbar_range(self, crange):
        """Asserts colorbar range matches min and max of crange parameter.

        Parameters
        ----------
        crange: tuple of (min, max) for colorbar
            If given empty tuple, asserts exactly 1 colorbar exists, but does
            not check values.

        Returns
        ----------
        Nothing (if checks pass) or raises error
        """
        # Check that images exist
        if not self.ax.images:
            assert False, "No image found on axes"

        # Get colorbars and check there's only one
        cb = self.get_colorbars()
        assert len(cb) == 1, "Exactly one colorbar should be displayed"

        # Check that colorbar range matches expected crange
        if crange:
            assert (
                cb[0].vmin == crange[0]
            ), "Colorbar minimum is not expected value:{0}".format(crange[0])
            assert (
                cb[0].vmax == crange[1]
            ), "Colorbar maximum is not expected value:{0}".format(crange[1])

    def _which_label(self, label, all_label_options):
        """Helper function for assert_legend_accuracy_classified_image
        Returns string that represents a category label for label.

        Parameters
        ----------
        label: string from legend to see if it contains an option in
            all_label_options
        all_label_options: list of lists
            Each internal list represents a class and said list is a list of
            strings where at least one string is expected to be in the legend
            label for this category.

        Returns
        ------
        string that is the first entry in the internal list which label is
        matched with. If no match is found, return value is None
        """
        for label_opts in all_label_options:
            for s in label_opts:
                if s in label:
                    return label_opts[0]
        return None

    def assert_legend_accuracy_classified_image(
        self, im_expected, all_label_options
    ):
        """Asserts legend correctly describes classified image on Axes ax,
        checking the legend labels and the values

        Parameters
        ----------
        im_expected: array of arrays with expected classified image on ax.
            Class values must start with 0, 1, 2, etc.
        all_label_options: list of lists
            Each internal list represents a class and said list is a list of
            strings where at least one string is expected to be in the legend
            label for this category. Internal lists must be in the same order
            as bins in im_expected, e.g. first internal list has the expected
            label options for class 0.

        Returns
        ----------
        Nothing (if checks pass) or raises error


        Notes
        ----------
        First compares all_label_options against the legend labels to find
        which element of all_label_options matches that entry. E.g. if the
        first legend entry has a match in the first list in all_label_options,
        then that legend entry corresponds to the first class (value 0).
        Then the plot image array is copied and the values are set to the
        legend label that match the values (i.e. the element in
        all_label_options). The same is done for the expected image array.
        Finally those two arrays of strings are compared. Passes if they match.
        """
        # Retrieve image array
        im_data = []
        if self.ax.get_images():
            im = self.ax.get_images()[0]
            im_data, im_cmap = im.get_array(), im.get_cmap()
        assert list(im_data), "No Image Displayed"

        # Retrieve legend
        legends = self.get_legends()
        assert legends, "No legend displayed"

        # Retrieve legend entries and find which element of all_label_options
        # matches that entry
        legend_dict = {}
        for p in [
            p
            for sublist in [leg.get_patches() for leg in legends]
            for p in sublist
        ]:
            label = p.get_label().lower()
            legend_dict[p.get_facecolor()] = self._which_label(
                label, all_label_options
            )

        # Check that each legend entry label is in one of all_label_options
        assert len([val for val in legend_dict.values() if val]) == len(
            all_label_options
        ), "Incorrect legend labels"

        # Create two copies of image array, one filled with the plot data class
        # labels (im_data_labels) and the other with the expected labels
        # (im_expected_labels)
        im_class_dict = {}
        for val in np.unique(im_data):
            im_class_dict[val] = legend_dict[im_cmap(im.norm(val))]
        im_data_labels = [
            [im_class_dict[val] for val in row] for row in im_data.data
        ]
        im_expected_labels = [
            [all_label_options[val][0] for val in row] for row in im_expected
        ]

        # Check that expected and actual labels match up
        assert np.array_equal(
            im_data_labels, im_expected_labels
        ), "Incorrect legend to data relation"

        # IMAGE TESTS/HELPER FUNCTIONS

    def get_plot_image(self):
        """Returns images stored on the Axes object as a list of numpy arrays.

        Returns
        -------
        im_data: List
            Numpy array of images stored on Axes object.
        """
        im_data = []
        if self.ax.get_images():
            im_data = self.ax.get_images()[0].get_array()
        assert list(im_data), "No Image Displayed"

        # If image array has 3 dims (e.g. rgb image), remove alpha channel
        if len(im_data.shape) == 3:
            im_data = im_data[:, :, :3]
        return im_data

    def assert_image(
        self, im_expected, im_classified=False, m="Incorrect Image Displayed"
    ):
        """Asserts the first image in Axes ax matches array im_expected

        Parameters
        ----------
        im_expected: Numpy Array
            Array containing the expected image data.
        im_classified: boolean
            Set to True image has been classified. Since classified images
            values can be reversed or shifted and still produce the same image,
            setting this to True will allow those changes.
        m: string
            String error message if assertion is not met.

        Returns
        ----------
        Nothing (if checks pass) or raises error
        """
        im_data = []
        if self.ax.get_images():
            im_data = self.ax.get_images()[0].get_array()
        assert list(im_data), "No Image Displayed"

        # If image array has 3 dims (e.g. rgb image), remove alpha channel
        if len(im_data.shape) == 3:
            im_data = im_data[:, :, :3]
        assert im_data.shape == im_expected.shape, "Incorrect Image Size"

        # If image is a classified image, allow for shifted or reversed values
        if im_classified:
            im_data_vals = np.unique(im_data)
            im_range = max(im_data_vals) - min(im_data_vals)
            offset = min(im_data_vals) - min(np.unique(im_expected))
            im_data = [val - offset for val in im_data]
            im_data_rev = [abs(val - im_range) for val in im_data]
            assert np.array_equal(im_data, im_expected) or np.array_equal(
                im_data_rev, im_expected
            ), m
        # If not im_classified, image array must exactly match expected array
        else:
            np.testing.assert_equal(im_data, im_expected), m

    def assert_image_full_screen(self, m="Image is stretched inaccurately"):
        """Asserts the first image in ax fills the entire axes window

        Parameters
        ----------
        m: error message if assertion is not met

        Returns
        ----------
        Nothing (if checks pass) or raises error with message m
        """
        ax_extent = list(self.ax.get_xlim() + self.ax.get_ylim())
        if self.ax.images:
            assert np.array_equal(self.ax.images[0].get_extent(), ax_extent), m
        else:
            assert False, "No image found on axes"
