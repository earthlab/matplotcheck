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
        """Helper function for assert_legend_labels
        Returns string that represents a category label for label.

        Parameters
        ----------
        label: string from legend to see if it contains an option in
            all_label_options
        all_label_options: list
            List should be from an internal list from a list of lists.
            Each internal list represents a class and said list is a list of
            strings where at least one string is expected to be in the legend
            label for this category.

        Returns
        ------
        string that is the first entry in the internal list which label is
        matched with. If no match is found, return value is None
        """
        for label_option in all_label_options:
            if label_option == label:
                return label_option
        return None

    def assert_raster_legend_labels(self, im_expected, all_label_options):
        """Asserts legend correctly describes classified image on Axes ax,
        checking the legend labels and the values

        Parameters
        ----------
        im_expected: array of arrays with expected classified image on ax.
        all_label_options: list of lists
            Each internal list represents a class and said list is a list of
            strings where at least one string is expected to be in the legend
            label for this category. Internal lists must be in the same order
            as bins in im_expected, e.g. first internal list has the expected
            label options for class 0.

        Returns
        ----------
        Nothing (if checks pass) or raises error
        """
        # Retrieve image array
        im_data = self.get_plot_image()

        assert list(im_data), "No Image Displayed"

        # Retrieve legend entries and find which element of all_label_options
        # matches that entry

        labels = self.get_legend_labels()

        assert len(labels) == len(all_label_options), (
            "Number of label options provided doesn't match the number of"
            " labels found in the image."
        )

        labels_check = [
            self._which_label(label, all_label_options[i])
            for i, label in enumerate(labels)
        ]

        # Check that each legend entry label is in one of all_label_options
        assert all(
            labels_check
        ), "Provided legend labels don't match labels found."

        # Check that expected and actual arrays data match up
        assert np.array_equal(
            im_data, im_expected
        ), "Expected image data doesn't match data in image."

        # IMAGE TESTS/HELPER FUNCTIONS

    def get_legend_labels(self):
        """Return labels from legend in a list

        Returns
        -------
        labels: List
            List of labels found in the legend of a raster plot.
        """

        # Retrieve legend
        legends = self.get_legends()
        assert legends, "No legend displayed"

        # Get each patch stored in the legends object
        patches = [leg.get_patches() for leg in legends]

        # Go through each patch to retrieve the labels from the legend
        return [
            label.get_label().lower()
            for sublist in patches
            for label in sublist
        ]

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
