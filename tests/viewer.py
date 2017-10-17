import logging
from os import path
from src.viewer import Viewer
import tkinter as tk
import unittest

class ViewerTestCases(unittest.TestCase):
    display_images = True
    root_tk = tk.Tk()

    def create_viewer(self):
        data_dir = path.join(path.dirname(__file__), 'data')
        return Viewer(data_dir, 1, log_level=logging.DEBUG, tk_root=self.root_tk)

    def test_viewer_init(self):
        """Instantiate a viewer."""
        v = self.create_viewer()

    def test_check_images(self):
        """Check image file inspection."""
        v = self.create_viewer()
        filenames = v.get_filenames()
        self.assertEqual(4, len(filenames), 'failed to find expected number of images')

    def test_viewer_display(self):
        """Cycle through images to display."""
        v = self.create_viewer()
        if self.display_images:
            for i in range(0, len(v.get_filenames())):
                logging.debug(('display', i))
                v.display_next()

