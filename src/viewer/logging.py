# Copyright (c) 2017 Jonathan Bredin
# MIT license http://opensource.org/licenses/MIT

import logging


def init_logging(log_level=logging.INFO):
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        level=log_level)
