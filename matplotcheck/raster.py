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

    def _check_label(self, labels, expected_labels):
        """Helper function for assert_legend_labels
        Tests each label in the legend to see if the text in expected labels
        matches the text found in the legend labels.

        Parameters
        ----------
        # TODO: update all parameters and associated parameter description
        labels: string from legend to see if it contains an option in
            expected_labels
        expected_labels: list of lists
            Each list within the main list should contain a list of strings
            that are expected to be found in each label in the plot
            legend that is being tested.
            TODO: clarify if this is or or "and" - ie i think it's or - is
            just makes sure that one of the words in the sublist of expected
            labels is in the plot legend

        Returns
        ------
        Dictionary ... #TODO update this return statement
        string that is the first entry in the internal list which label is
        matched with. If no match is found, return value is None
        """
        # TODO: return boolean instead of a none value - true if it matches,
        #  false if it does not match

        #
        # for label_option in expected_labels:
        #     if label_option == label:
        #         return label_option

        label_check = {}

        # Iteratively test each label found in the plot legend to see if it is
        # in the list of expected labels
        for i, label in enumerate(labels):
            test_output = any(
                label in expected_label
                for expected_label in expected_labels[i]
            )
            label_check[label] = test_output

        return label_check

    def assert_raster_legend_labels(self, im_expected, expected_labels):
        """Asserts legend correctly describes classified image on Axes ax,
        checking the legend labels and the values

        Parameters
        ----------
        im_expected: array of arrays with expected classified image on ax.
        expected_labels: list of lists
            Each sublist within the expected_labels list contains the word
            or word variations expected to be found in the legend labels of
            the plot being tested. Example list: [["gain", "increase"]]
            would be provided if you wanted to test that the word "gain" OR
            "increase"  were found in the first legend element.
            TODO: i think it's or but let's just clarify it's not "and"
            TODO: we should have tests that check what happens if someone
            provides only 2 sublist but there are three legend labels.
            Sublists must be in the same order as the legend elements are
            in. EXAMPLE: the first sublist will map to the first labeled item
            in a plot legend.

        Returns
        ----------
        Nothing (if checks pass) or raises assertion error
        """

        # TODO add test for a plot with no image in it. get_plot_image should
        # return an error

        # Retrieve image array
        im_data = self.get_plot_image()

        # TODO: We shouldn't need these tests because they happen in
        #  get_plot_image already. But we should improve the output message in
        # get_plot image to be something more expressive
        # assert list(im_data), "No Image Displayed"

        labels = self.get_legend_labels()

        # TODO: i think this should be a try, catch / return value error
        assert len(labels) == len(expected_labels), (
            "Number of label options provided doesn't match the number of"
            " labels found in the image."
        )

        # TODO: this currently only returns a list of values. It would be
        #  better if it returns a dictionary with the key being each
        #  label being tested and the value being a boolean (True if there
        #  is a match, False if there is no match)

        labels_dict = self._check_label(labels, expected_labels)

        # labels_check = [
        #     self._check_label(label, expected_labels[i])
        #     for i, label in enumerate(labels)
        # ]

        # TODO: this now becomes a bit more tricky but we need to 1) test that
        # each label is true - if one is false, then return useful message
        # stating which label is incorrect.

        # Pull out any labels that failed the above test for final printing
        # below
        bad_labels = {
            key: labels_dict[key]
            for key in labels_dict
            if not labels_dict[key]
        }

        # TODO: raise assertion error (value error?) and print out a list of
        #  labels that are wrong ONLY if some are wrong
        if bad_labels:
            # get just the labels that are
            bad_keys = [str(a_key) for a_key in bad_labels.keys()]
            raise ValueError(
                "Oops. It looks like atleast one of your legend "
                "labels is incorrect. Double check the "
                "following label(s): {"
                "}".format(bad_keys)
            )

        # Check that each legend entry label is in one of expected_labels
        # assert all(
        #     labels_check
        # ), "Provided legend labels don't match labels found."

        # TODO: once we get the above working, let's then add another layer
        #  where we grab the RGB values and also add that to the dictionary
        # At that point we can test whether the colors in the plot array, map
        # to the legend patch colors and in turn the expected image

        # Check that expected and actual arrays data match up
        assert np.array_equal(
            im_data, im_expected
        ), "Expected image data doesn't match data in image."

        # TODO: warning -- proj_create: init=epsg:/init=IGNF: syntax not
        #  supported in non-PROJ4 emulation mode - where is this coming from?

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
