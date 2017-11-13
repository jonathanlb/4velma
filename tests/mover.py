import logging, shutil, tempfile, unittest
from os import path
from src.viewer import Mover
from src.viewer.logging import init_logging


card_dir_name = 'cardmount'

class MoverTestCases(unittest.TestCase):

  def create_mover(self):
    src_dir = path.join(self.mount_dir, card_dir_name)
    return Mover(src_dir, self.snk_dir, mounts=self.mounts)

  def setUp(self):
    init_logging(logging.DEBUG)
    self.mount_dir = tempfile.mkdtemp()
    self.snk_dir = tempfile.mkdtemp()

    self.mounts = path.join(self.mount_dir, 'mounts')
    f = open(self.mounts, 'x')
    f.close()

  def tearDown(self):
    try:
      shutil.rmtree(self.mount_dir)
    except: IOError

    try:
      shutil.rmtree(self.snk_dir)
    except: IOError

  def test_create(self):
    mover = self.create_mover()
    with mover:
      self.assertFalse(mover.is_input_mounted(self.mounts),
        msg='Could not open unready mount file {}'.format(self.mounts))
      self.assertTrue(mover.mount_wait(0, wait_for_mounted=False),
        msg='Expected no filesystem mount wfm=False')
      self.assertFalse(mover.mount_wait(0, wait_for_mounted=True),
        msg='Expected no filesystem mount wfm=True')

  def test_move(self):
    mover = self.create_mover()
    with mover:
      # simulate mounting
      shutil.os.mkdir(mover.src_dir)
      src_filename = path.join(mover.src_dir, 'empty.jpg')
      snk_filename = path.join(mover.snk_dir, 'empty.jpg')
      f = open(src_filename, 'x')
      f.write('testing\n')
      f.close()
      
      self.assertFalse(path.exists(snk_filename),
        msg='File copied before simulated mount')
      f = open(self.mounts, 'a')
      f.write('blah blah\n/dev/sdb1 ')
      f.write(path.join(self.mount_dir, card_dir_name))
      f.write('\nyadda yadda yadda\n')
      f.close()

      self.assertTrue(mover.is_input_mounted(self.mounts),
        msg='Could not open mount file {}'.format(self.mounts))
      self.assertIsNotNone(mover.mount_wait(0),
        msg='Failed to wait for mount')
      mover.copy_files()
      self.assertTrue(path.exists(snk_filename),
        msg='File did not copy over')
