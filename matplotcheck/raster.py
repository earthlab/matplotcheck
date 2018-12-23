import numpy as np

from .base import PlotTester


class RasterTester(PlotTester):
    """A PlotTester for spatial raster plots.

	Parameters
	----------
	ax: ```matplotlib.axes.Axes``` object

	"""

    def __init__(self, ax):
        """Initialize the raster tester"""
        super(RasterTester, self).__init__(ax)

    def get_colorbars(self):
        """Returns a list of colorbars on Axes ax

		Returns
		-------
		cb: list of colorbars on axes. If no colorbars exist, Returns an empty list.
		"""
        cb = [im.colorbar for im in self.ax.images if im.colorbar]
        return cb

    def assert_colorbar_range(self, crange):
        """Asserts colorbar range to match min and max defined in crange.

		Parameters
		----------
		crange: tuple of (min, max) for colorbar. 
			if empty tuple: asserts exactly 1 colobar exists, but does not check values.
		"""
        cb = self.get_colorbars()
        assert len(cb) == 1, "Exactly one colorbar should be displayed"
        if crange:
            assert (
                cb[0].vmin == crange[0]
            ), "Colorbar minimum is not expected value:{0}".format(crange[0])
            assert (
                cb[0].vmax == crange[1]
            ), "Colorbar maximum is not expected value:{0}".format(crange[1])

    def _which_label(self, label, all_label_options):
        """helper function for assert_legend_accuracy_classified_image
		Returns string that represents a category label for label.

		Parameters
		----------
		label: string to see if it contains an option in all_label_options
		all_label_options: list of lists. Each internal list represents a classification category.
			Said list is a list of strings where at least one string is expected to be in the legend label for this category.
		
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
		im_expected: array of arrays with expected classified image on ax. Classification must start with bin 0.
		all_label_options: list of lists. Each internal list represents a classification category.
			Said list is a list of strings where at least one string is expected to be in the legend label for this category.
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
            legend_dict[p.get_facecolor()] = self._which_label(
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

        ### IMAGE TESTS/HELPER FUNCTIONS ###

    def assert_image(
        self, im_expected, im_classified=False, m="Incorrect Image Displayed"
    ):
        """Asserts the first image in Axes ax matches im_expected

		Parameters
		----------
		im_expected: array containing an expected image
		im_classified: boolean for if image must be exact or if image has been classified. Since classified
			images values can be reversed or shifted and still produce the same image, setting this to True
			will allow those changes.
		m: string error message if assertion is not met
		"""
        im_data = []
        if self.ax.get_images():
            im_data = self.ax.get_images()[0].get_array()
        assert list(im_data), "No Image Displayed"

        # remove alpha channel for rgb image
        if len(im_data.shape) == 3:
            im_data = im_data[:, :, :3]
        assert im_data.shape == im_expected.shape, "Incorrect Image Size"

        if im_classified:
            im_data_vals = np.unique(im_data)
            im_range = max(im_data_vals) - min(im_data_vals)
            offset = min(im_data_vals) - min(np.unique(im_expected))
            im_data = [val - offset for val in im_data]
            im_data_rev = [abs(val - im_range) for val in im_data]
            assert np.array_equal(im_data, im_expected) or np.array_equal(
                im_data_rev, im_expected
            ), m
        else:
            np.testing.assert_equal(im_data, im_expected), m

    def assert_image_full_screen(self, m="Image is stretched inaccurately"):
        """Asserts the first image in ax expands the entire axes

		Parameters
		----------
		m: error message if assertion is not met
		"""
        ax_extent = list(self.ax.get_xlim() + self.ax.get_ylim())
        if self.ax.images:
            assert np.array_equal(self.ax.images[0].get_extent(), ax_extent), m
        else:
            assert False, "No image found on axes"
