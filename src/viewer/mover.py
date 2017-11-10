# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

import argparse
import logging
import os, select, subprocess, time
from operator import xor
from pathlib import Path


class Mover:
  """
  Strategy: monitor directory for changes
  """
  def __init__(self, src_dir, snk_dir, mounts='/proc/self/mounts'):
    self.src_dir = src_dir
    self.snk_dir = snk_dir
    self.mounts = mounts
    self.mount_f = None
    self.pollster = None

  def __enter__(self):
    return

  def __exit__(self, type, value, traceback):
    self._close_polling_()
 
  def _close_polling_(self):
    if self.mount_f:
      self.mount_f.close()
      self.mount_f = None
      self.pollster = None

  def _get_time_(self):
    return int(time.clock() * 1000)

  def copy_files(self):
    exec_cmd = '-exec cp -n -v {} ' + self.snk_dir + ' ;'
    cmd = 'find ' + self.src_dir + \
      ' -type f -iname *.jpg ' + exec_cmd + \
      ' -o -iname *.jpeg ' + exec_cmd;
    proc = subprocess.Popen(
      cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = ''
    try:
      logging.debug(('copying... ', cmd))
      proc.wait()
      for line in proc.stdout.readlines():
        logging.info(line)
      stderr = str(proc.stderr.readlines())
    finally:
      if proc.stdout:
        proc.stdout.close()
      if proc.stderr:
        proc.stderr.close()

    if proc.returncode:
      raise IOError('calling "{}" : {}'.format(cmd, stderr))

  def is_input_mounted(self, mount_fd):
    f = open(mount_fd, 'r')
    lines = f.readlines()
    f.close()
    return any(line.find(self.src_dir) >= 0 for line in lines)

  def run(self, poll_millis=60000):
    try:
      while True:
        while not self.mount_wait(poll_millis, wait_for_mounted=True):
          'Do nothing'
        self.copy_files()
        while not self.mount_wait(poll_millis, wait_for_mounted=False):
          'Do nothing'
    except KeyboardInterrupt:
      logging.info('Interrupted, shutting down')

  def mount_wait(self, millis, wait_for_mounted=True):

    waited = 0
    while waited <= millis:
      start_millis = self._get_time_()

      self.mount_f = open(self.mounts, 'r')
      self.pollster = select.poll()
      self.pollster.register(self.mount_f, select.POLLERR | select.POLLPRI)

      wait_millis = max(millis - waited, 0)
      logging.info(('Waiting millis', wait_millis, 'for_mount?', wait_for_mounted))
      events = self.pollster.poll(wait_millis)
      self._close_polling_()
      waited += self._get_time_() - start_millis

      # fds from poll() seem to be reused and invalid?
      is_mounted = self.is_input_mounted(self.mounts)

      if xor(is_mounted, not wait_for_mounted):
        return True
    return False

  @staticmethod
  def parse_args():
    parser = argparse.ArgumentParser(
      description='Watch and copy image files from SD-card reader')
    parser.add_argument('--mountpoint', '-i',
      required=True, help='Linux mount-point directory, e.g. /mnt/card')
    parser.add_argument('--destination', '-o',
      required=True, help='image destination')
    return parser.parse_args()
