import logging
from os import path
from src.viewer import Viewer
from src.viewer.logging import init_logging
import tkinter as tk
import unittest


class ViewerTestCases(unittest.TestCase):
    display_images = True
    root_tk = tk.Tk()
    init_logging(logging.DEBUG)

    def create_viewer(self, data_dir=None):
        if not data_dir:
            data_dir = path.join(path.dirname(__file__), 'data')
        return Viewer(data_dir, 1, full_screen=True, tk_root=self.root_tk)

    def test_viewer_init(self):
        """Instantiate a viewer."""
        v = self.create_viewer()

    def test_check_images(self):
        """Check image file inspection."""
        v = self.create_viewer()
        filenames = v.get_filenames()
        self.assertEqual(4, len(filenames), 'failed to find expected number of images')

    def test_check_no_images(self):
        """Check error handling when no images present."""
        # Point to some directory w/o pictues.
        v = self.create_viewer(data_dir=path.dirname(__file__))
        self.assertRaises(Exception, v.next_image)

    def test_viewer_display(self):
        """Cycle through images to display."""
        v = self.create_viewer()
        if self.display_images:
            for i in range(0, len(v.get_filenames())):
                logging.debug(('display', i))
                v.display_next()

    def test_scaling(self):
        v = self.create_viewer()
        img = v.next_image(0)
        original_aspect = img.width / img.height
        scaled_image = v.resize_image(img)
        scaled_aspect = scaled_image.width / scaled_image.height

        logging.debug('{}x{} ({}) to {}x{} ({})'.format(img.width, img.height, original_aspect, scaled_image.width, scaled_image.height, scaled_aspect))
        self.assertTrue(scaled_image.width == v.width or scaled_image.height == v.height,
                        'expecting either height or width of image to be screen size')
        self.assertAlmostEqual(original_aspect, scaled_aspect, places=2, msg='scaling preserves aspect')
