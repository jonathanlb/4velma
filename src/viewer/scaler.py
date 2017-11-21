# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

import logging
import tkinter as tk
from PIL import Image, ImageTk

class Scaler:
    background = 'black'

    def __init__(self, tk_root, dimensions=None):
        self._tk_root = tk_root
        if dimensions:
            self.resize(dimensions)
        else:
            self._width = tk_root.winfo_screenwidth()
            self._height = tk_root.winfo_screenheight()
            logging.debug(('tk width', self._width, 'height', self._height))

        self._panel = tk.Label(tk_root)
        self._panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

    def get_height(self):
        return self._height

    def get_panel(self):
        return self._panel

    def get_width(self):
        return self._width

    def resize(self, dimensions, image=None):
        self._width = dimensions[0]
        self._height = dimensions[1]
        logging.debug(('scaler resize width', self._width, 'height', self._height))

        if image:
            self.set_image(image)

    def resize_image(self, image):
        width = self.get_width()
        height = self.get_height()
        render_width = int(height * image.width / image.height)
        render_height = int(width * image.height / image.width)

        if render_width > width:
            render_width = width
        else:
            render_height = height

        logging.debug(('resize_image', render_width, render_height))
        return image.resize((render_width, render_height), Image.BICUBIC)

    def set_image(self, image):
        displayed_image = self.resize_image(image)
        self._tk_image = ImageTk.PhotoImage(displayed_image)
        # borderwidth=0 prevents cascade of redraw events/hacking dimensions.
        self._panel.configure(bg=self.background, borderwidth=0,
                              image=self._tk_image)
