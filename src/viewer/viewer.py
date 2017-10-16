# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

import logging
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk


class Viewer:
    height = None
    image_idx = 0
    """Keep reference to image to prevent tkinter from cleaning it up."""
    image = None
    panel = None
    root = None
    tk_image = None
    width = None

    def __init__(self, directory, seconds):
        self.directory = directory
        self.seconds = seconds
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                            level=logging.INFO)

    @staticmethod
    def _is_image_(filename):
        """Image file predicate."""
        suffixes = ['.jpg', '.png']
        return any(x for x in suffixes if filename.suffix == x)

    def display_loop(self):
        """Display the next image and schedule next step of looping."""
        self.display_next()
        self.root.after(self.seconds*1000, self.display_loop)

    def display_next(self):
        """Configure the root pane if necessary and load the next image into rotation."""
        self.image = self.next_image()
        if (self.width or self.height):
            self.image = self.image.resize((self.width, self.height))

        if not self.root:
            self.root = tk.Tk()
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.panel = tk.Label(self.root, image=self.tk_image)
            self.panel.bind('<Configure>', self.resize_image)
            self.panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        else:
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.panel.configure(image=self.tk_image)

    def get_filenames(self):
        """Scan the image directory for image file names."""
        p = Path(self.directory)
        return [x for x in p.iterdir() if not x.is_dir() and self._is_image_(x)]

    def next_image(self):
        """Load the next image in the directory using the current view of the directory."""
        filenames = self.get_filenames()
        # Prevent out-of-bounds when files are removed.
        self.image_idx = self.image_idx % len(filenames)
        filename = filenames[self.image_idx]
        img = Image.open(filename)
        self.image_idx = (self.image_idx + 1) % len(filenames)
        return img

    def resize_image(self, event):
        """
        Respond to tkinter resizing events, clipping by mysterious magic number
        to prevent cascade of resize events.
        """
        self.width = event.width - 4
        self.height = event.height - 4
        logging.debug(('width', self.width, 'height', self.height))
        self.image = self.image.resize((self.width, self.height))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.panel.configure(image=self.tk_image)

    def run(self):
        """Enter non-terminating main loop, scheduling image updates."""
        self.display_loop()
        logging.info('Entering tkinter main loop.')
        self.root.mainloop()
