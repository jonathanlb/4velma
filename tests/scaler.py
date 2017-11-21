# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

import logging
import tkinter as tk
import unittest
from PIL import Image
from src.viewer.scaler import Scaler


class ScalerTestCases(unittest.TestCase):
    def create_scaler(self, dim):
        tk_root = tk.Tk()
        dim = (640, 480)
        return Scaler(tk_root, dim)

    def test_resize(self):
        dim = (640, 480)
        v = self.create_scaler(dim)
        new_dim = (300, 200)
        img = Image.new('RGB', (200, 300))
        v.resize(new_dim, img)
        self.assertEqual(new_dim[0], v.get_width())
        self.assertEqual(new_dim[1], v.get_height())

        v.resize(dim)
        self.assertEqual(dim[0], v.get_width())
        self.assertEqual(dim[1], v.get_height())

    def test_scaling(self):
        dim = (640, 480)
        v = self.create_scaler(dim)

        def scale_image(img):
            original_aspect = img.width / img.height
            scaled_image = v.resize_image(img)
            scaled_aspect = scaled_image.width / scaled_image.height

            logging.debug('{}x{} ({}) to {}x{} ({})'.format(img.width, img.height, original_aspect, scaled_image.width, scaled_image.height, scaled_aspect))
            self.assertTrue(scaled_image.width == v.get_width() or scaled_image.height == v.get_height(),
                            'expecting either height or width of image to be screen size')
            self.assertAlmostEqual(original_aspect, scaled_aspect, places=2, msg='scaling preserves aspect')
            self.assertEqual(dim[0], v.get_width())
            self.assertEqual(dim[1], v.get_height())

        scale_image(Image.new('RGB', (300, 200)))
        scale_image(Image.new('RGB', (200, 300)))
