# ~*~ encoding: utf-8 ~*~
from __future__ import absolute_import

import logging
import sys
import codecs


class ExactLevel(object):
    def __init__(self, level):
        self._level = level

    def filter(self, record):
        return record.levelno == self._level


def setup_handlers(logger, stdout=None, stderr=None):
    if stdout is None:
        stdout = codecs.getwriter('utf-8')(sys.stdout)
    if stderr is None:
        stderr = codecs.getwriter('utf-8')(sys.stderr)

    stdout_handler = logging.StreamHandler(stream=stdout)
    stdout_handler.addFilter(ExactLevel(logging.INFO))
    stderr_handler = logging.StreamHandler(stream=stderr)
    stderr_handler.addFilter(ExactLevel(logging.ERROR))
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)