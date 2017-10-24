# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

import argparse
import logging
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk


class Viewer:
    # Keep references to images to prevent GC from reclaiming from tkinter.
    background = 'black'
    """Scaled image to display"""
    display_image = None
    height = None
    image_idx = 0
    """Image read from disk"""
    image = None
    panel = None
    """Scaled image to for TK"""
    tk_image = None
    width = None

    def __init__(self, directory, seconds, full_screen=False,
                 tk_root=None):
        self.directory = directory
        self.seconds = seconds
        if tk_root:
            self.root = tk_root
        else:
            self.root = tk.Tk()
            self.root.bind('<Key>', self.handle_keypress)

        if full_screen:
            self.root.wm_overrideredirect(True)
            # self.root.attributes('-fullscreen', True)
            self.width = self.root.winfo_screenwidth()
            self.height = self.root.winfo_screenheight()

        self.root.configure(bg=self.background, highlightthickness=0)

    @staticmethod
    def _is_image_(filename):
        """Image file predicate."""
        suffixes = ['.gif', '.jpg', '.png']
        return any(x for x in suffixes if filename.suffix.lower() == x)

    def display_loop(self):
        """Display the next image and schedule next step of looping."""
        self.display_next()
        self.root.after(self.seconds*1000, self.display_loop)

    def display_next(self):
        """
        Configure the root pane if necessary and load the next image
        into rotation.
        """
        self.image = self.next_image()
        if self.width and self.height:
            self.displayed_image = self.resize_image()
        else:
            self.displayed_image = self.image
            self.height = self.image.height
            self.width = self.image.width

        self.tk_image = ImageTk.PhotoImage(self.displayed_image)

        if not self.panel:
            self.panel = tk.Label(self.root, image=self.tk_image)
            self.panel.bind('<Configure>', self.resize_window)
            self.panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.panel.configure(bg=self.background, image=self.tk_image)

    def get_filenames(self):
        """Scan the image directory for image file names."""
        p = Path(self.directory)
        return [x for x in p.iterdir() if not x.is_dir() and self._is_image_(x)]

    def handle_keypress(self, event):
        """
        Allow the user to quit with q; advance picture with f or space;
        replay last with d.  Ignore case.
        """
        logging.debug(('key', event, event.char))
        cmd = event.char.lower()
        if cmd == 'd':
            self.image_idx -= 2
            self.display_next()
        elif cmd == 'f' or cmd == ' ':
            self.display_next()
        elif cmd == 'q':
            self.root.quit()

    def next_image(self, idx=None):
        """
        Load the next image in the directory using the current view of
        the directory.
        """
        filenames = self.get_filenames()
        if len(filenames) <= 0:
            raise Exception('No files found in {}'.format(self.directory))

        if idx is None:
            # Prevent out-of-bounds when files are removed.
            self.image_idx = self.image_idx % len(filenames)
            idx = self.image_idx
            self.image_idx = (self.image_idx + 1) % len(filenames)

        filename = filenames[idx]
        logging.debug(('loading image', filename, idx))
        return Image.open(filename)

    def resize_image(self, image=None):
        """
        Resize the active image, or the image argument to fill the
        viewing area.
        """
        if image is None:
            image = self.image
 
        render_width = int(self.height * image.width / image.height)
        render_height = int(self.width * image.height / image.width)

        if (render_width > self.width):
           render_width = self.width
        else:
           render_height = self.height

        logging.debug(('resize', render_width, render_height))
        return image.resize((render_width, render_height), Image.BICUBIC)

    def resize_window(self, event):
        """Respond to tkinter resizing events."""
        self.width = event.width
        self.height = event.height
        logging.debug(('width', self.width, 'height', self.height))
        self.displayed_image = self.resize_image()
        self.tk_image = ImageTk.PhotoImage(self.displayed_image)
        # borderwidth=0 prevents cascade of redraw events/hacking dimensions.
        self.panel.configure(bg=self.background, borderwidth=0,
                             image=self.tk_image)

    def run(self):
        """Enter non-terminating main loop, scheduling image updates."""
        self.display_loop()
        logging.info('Entering tkinter main loop.')
        self.root.mainloop()

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
            description='Display pictures for your grandma.')
        parser.add_argument('--fullscreen', '-f', dest='fullscreen',
                            action='store_true', help='scale to use full screen')
        parser.add_argument('--input', '-i',
                            required=True, help='directory containing images')
        parser.add_argument('--duration', '-d', type=int, default=60,
                            required=False, help='display pictures for n seconds, default 60s')
        return parser.parse_args()