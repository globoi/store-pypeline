# ~*~ encoding: utf-8 ~*~
from __future__ import absolute_import

import logging
import sys
import codecs


class InLevel(object):
    def __init__(self, level_list):
        self._level_list = level_list

    def filter(self, record):
        return record.levelno in self._level_list


def setup_handlers(logger):
    stdout = codecs.getwriter('utf-8')(sys.stdout)
    stderr = codecs.getwriter('utf-8')(sys.stderr)

    stdout_handler = logging.StreamHandler(stream=stdout)
    stdout_handler.addFilter(InLevel([logging.INFO]))
    stdout_handler.setFormatter(logging.Formatter())
    logger.addHandler(stdout_handler)
    stderr_handler = logging.StreamHandler(stream=stderr)
    stderr_handler.addFilter(InLevel([logging.ERROR]))
    stderr_handler.setFormatter(logging.Formatter())
    logger.addHandler(stderr_handler)