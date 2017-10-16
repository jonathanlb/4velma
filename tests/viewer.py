import unittest
from os import path
from src.viewer import Viewer


class ViewerTestCases(unittest.TestCase):
    display_images = True

    @staticmethod
    def _create_viewer_():
        data_dir = path.join(path.dirname(__file__), 'data')
        return Viewer(data_dir, 1)

    def test_viewer_init(self):
        """Instantiate a viewer."""
        v = self._create_viewer_()

    def test_check_images(self):
        """Check image file inspection."""
        v = self._create_viewer_()
        filenames = v.get_filenames()
        self.assertEqual(4, len(filenames), 'failed to find expected number of images')

    def test_viewer_display(self):
        """Cycle through images to display."""
        v = self._create_viewer_()
        if self.display_images:
            for i in range(0, len(v.get_filenames())):
                v.display_next()

