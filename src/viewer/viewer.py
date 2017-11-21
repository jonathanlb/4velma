# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

import argparse
import logging
import os
from pathlib import Path
from src.viewer.scaler import Scaler
from src.viewer.logging import init_logging
from tkinter import filedialog
from threading import RLock
import tkinter as tk
from PIL import Image


class Viewer:
    background = 'black'
    image_idx = 0
    image_filename = None
    """Image read from disk"""
    image = None
    lock = None
    panel = None

    def __init__(self, directory, seconds, full_screen=False,
                 tk_root=None):
        self.directory = directory
        self.seconds = seconds
        if tk_root:
            self.root = tk_root
        else:
            self.root = tk.Tk()
            self.root.bind('<Key>', self.handle_keypress)

        self._scaler = Scaler(self.root)
        self._scaler.background = self.background
        if full_screen:
            self.root.wm_overrideredirect(True)
            # self.root.attributes('-fullscreen', True)
        self._scaler.get_panel().bind('<Configure>', self.resize_window)

        self.root.configure(bg=self.background, highlightthickness=0)
        self.lock = RLock()

    def __enter__(self):
        return

    def __exit__(self, type, value, traceback):
        """Release resources."""
        self.lock.acquire()
        if self.image:
            try:
                self.image.close()
            except Exception as e:
                logging.debug('__exit__ failure {}'.format(e))
                'do nothing'
        self.image = None
        self.image_filename = None
        self.lock.release()

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
        logging.debug('lock display_next')
        self.lock.acquire()
        self.__exit__(None, None, None)
        self.image, self.image_filename = self.next_image()
        # self._scaler.set_image(self.image)
        self._scaler.resize((self.image.width, self.image.height), self.image)
        self.lock.release()
        logging.debug('release display_next')

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
            logging.debug('lock handle_keypress previous')
            self.lock.acquire()
            self.image_idx -= 2
            self.display_next()
            self.lock.release()
            logging.debug('release handle_keypress previous')
        elif cmd == 'f' or cmd == ' ':
            self.display_next()
        elif cmd == 'q':
            self.root.quit()
        elif cmd == '\x7f' or cmd == '\x08':
            self.show_delete()
        elif cmd == '<':
            self.rotate_image(self.image, self.image_filename, 90)
        elif cmd == '>':
            self.rotate_image(self.image, self.image_filename, -90)

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
        # Pillow seems to have a bug leaving open file handles.
        # The following with __exit__ appears to clean up, but still
        # produces debug warnings.
        # https://stackoverflow.com/questions/38541735/pillownumpyunittest-gives-a-resourcewarning-does-this-indicate-a-leak
        with open(str(filename), 'rb') as im_handle:
            im = Image.open(im_handle)
            return im.copy(), filename

    def resize_window(self, event):
        """Respond to tkinter resizing events."""
        logging.debug(('resize_window', event.width, event.height))
        self._scaler.resize((event.width, event.height), self.image)

    def rotate_image(self, image, filename, degrees):
        """Rotate the image, save it, and attempt to redisplay it."""
        logging.debug('lock rotate')
        self.lock.acquire()
        image = image.rotate(degrees, expand=True)
        image.save(filename)
        self.image_idx -= 1
        self.display_next()
        self.lock.release()
        logging.debug('release rotate')

    def run(self):
        """Enter non-terminating main loop, scheduling image updates."""
        self.display_loop()
        logging.info('Entering tkinter main loop.')
        self.root.mainloop()

    def show_delete(self):
        """
        Show a dialog to preview and delete files.
        TODO: Replace 'Open' label on button with delete.
        TODO: Show title on dialog.  filedialog rot?
        TODO: Limit to image types under selected directory.
        """
        files = filedialog.askopenfiles(
            initialdir=self.directory,
            parent=self.root,
            mode='rb',
            title='Select files to delete...')
        if files:
            logging.debug('lock delete')
            self.lock.acquire()
            for file in files:
                file_name = file.name
                logging.info('deleting {}'.format(file_name))
                try:
                    os.remove(file_name)
                except OSError as ose:
                    logging.error('cannot delete {}: {}'.format(file_name, ose))
            self.display_next()
            self.lock.release()
            logging.debug('release delete')

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
        parser.add_argument('--verbose', '-v', dest='verbose',
                            action='store_true', help='log debugging information')
        args = parser.parse_args()
        if args.verbose:
            init_logging(logging.DEBUG)
        else:
            init_logging(logging.INFO)
        return args
