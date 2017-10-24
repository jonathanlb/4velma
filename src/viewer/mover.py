# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

import argparse
import logging
from os import path
import pathlib
import re
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Mover(FileSystemEventHandler):
    """
    Watch a directory/mount point for image files and copy new ones to a sink directory.
    """

    def __init__(self, input, output):
        self.input = self._make_absolute_path_(input)
        self.output = self._make_absolute_path_(output)
        self.files = {}

    @staticmethod
    def _make_absolute_path_(f):
        if not f.startswith('/'):
            return path.join(path.abspath(path.curdir), f)
        else:
            return f

    def _add_dir_(self, dir_name):
        for f in pathlib.os.listdir(dir_name):
            self._add_file_(f)

    def _add_file_(self, file_name):
        logging.info('adding {}'.format(file_name))
        self.files[file_name] = file_name
        return

    def copy_file(self, key):
        src = path.join(self.input, key)
        dst = path.join(self.output, key)
        logging.info('copy {} -> {}'.format(src, dst))
        shutil.copy(src, dst)
        return

    def get_file_key(self, file_name):
        if file_name.startswith(self.input):
            result = file_name.replace(self.input, '')
        elif file_name.startswith(self.output):
            result = file_name.replace(self.output, '')
        else:
            return None
        return re.sub('^/', '', result)

    def has_file(self, file_name):
        return self.files.get(file_name) is not None

    def on_created(self, event):
        file_name = event.src_path
        key = self.get_file_key(file_name)
        if not self.has_file(key):
            self._add_file_(key)
            self.copy_file(key)

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
            description='Copy pictures from one directory into another.')
        parser.add_argument('--input', '-i',
                            required=True, help='source directory')
        parser.add_argument('--output', '-o',
                            required=True, help='sink directory')
        return parser.parse_args()

    def run(self):
        self._add_dir_(self.output)
        observer = Observer()
        observer.schedule(self, self.input, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()