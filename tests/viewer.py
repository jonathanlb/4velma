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
        with self.create_viewer():
            'Do nothing'

    def test_check_images(self):
        """Check image file inspection."""
        v = self.create_viewer()
        with v:
            filenames = v.get_filenames()
        self.assertEqual(4, len(filenames), 'failed to find expected number of images')

    def test_check_no_images(self):
        """Check error handling when no images present."""
        # Point to some directory w/o pictues.
        v = self.create_viewer(data_dir=path.dirname(__file__))
        with v:
            self.assertRaises(Exception, v.next_image)

    def test_viewer_display(self):
        """Cycle through images to display."""
        v = self.create_viewer()
        with v:
            if self.display_images:
                for i in range(0, len(v.get_filenames())):
                    logging.debug(('display', i))
                    v.display_next()

