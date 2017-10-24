import logging
from os import path
from src.viewer import Mover
from src.viewer.logging import init_logging
import unittest


class MoverTestCases(unittest.TestCase):
    init_logging(logging.DEBUG)

    def test_mover_init(self):
        d = path.dirname(__file__)
        src_dir = path.join(d, 'data/src')
        sink_dir = path.join(d, 'data/snk')
        m = Mover(src_dir, sink_dir)
        self.assertFalse(m.has_file('foo.txt'))
