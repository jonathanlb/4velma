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
    tk_image = None
    width = None

    def __init__(self, directory, seconds, full_screen=False, log_level=logging.INFO, tk_root=None):
        self.directory = directory
        self.seconds = seconds
        if tk_root:
            self.root = tk_root
        else:
            self.root = tk.Tk()

        if full_screen:
            self.root.wm_overrideredirect(True)
            self.width = self.root.winfo_screenwidth()
            self.height = self.root.winfo_screenheight()

        # TODO: no global config
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                            level=log_level)

    @staticmethod
    def _is_image_(filename):
        """Image file predicate."""
        suffixes = ['.gif', '.jpg', '.png']
        return any(x for x in suffixes if filename.suffix == x)

    def display_loop(self):
        """Display the next image and schedule next step of looping."""
        self.display_next()
        self.root.after(self.seconds*1000, self.display_loop)

    def display_next(self):
        """Configure the root pane if necessary and load the next image into rotation."""
        self.image = self.next_image()
        if self.width and self.height:
            self.image = self.resize_image()
        else:
            self.height = self.image.height
            self.width = self.image.width

        if not self.tk_image:
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.panel = tk.Label(self.root, image=self.tk_image)
            self.panel.bind('<Configure>', self.resize_window)
            self.panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        else:
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.panel.configure(image=self.tk_image)

    def get_filenames(self):
        """Scan the image directory for image file names."""
        p = Path(self.directory)
        return [x for x in p.iterdir() if not x.is_dir() and self._is_image_(x)]

    def next_image(self, idx=None):
        """Load the next image in the directory using the current view of the directory."""
        filenames = self.get_filenames()

        if idx is None:
            # Prevent out-of-bounds when files are removed.
            self.image_idx = self.image_idx % len(filenames)
            idx = self.image_idx
            self.image_idx = (self.image_idx + 1) % len(filenames)

        filename = filenames[idx]
        logging.debug(('loading image', filename, idx))
        return Image.open(filename)

    def resize_image(self, image=None):
        """TODO: ensure aspect ratio is preserved."""
        if image is None:
            image = self.image
        image_ratio = image.height / image.width
        viewer_ratio = self.height / self.width
        if image_ratio < viewer_ratio:
            return image.resize((int(image_ratio * self.height), self.height), Image.BICUBIC)
        else:
            return image.resize((self.width, int(image_ratio * self.width)), Image.BICUBIC)

    def resize_window(self, event):
        """
        Respond to tkinter resizing events, clipping by mysterious magic number
        to prevent cascade of resize events.
        """
        self.width = event.width - 4
        self.height = event.height - 4
        logging.debug(('width', self.width, 'height', self.height))
        self.image = self.resize_image()
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.panel.configure(image=self.tk_image)

    def run(self):
        """Enter non-terminating main loop, scheduling image updates."""
        self.display_loop()
        logging.info('Entering tkinter main loop.')
        self.root.mainloop()
