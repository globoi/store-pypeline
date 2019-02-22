# ~*~ encoding: utf-8 ~*~
from __future__ import absolute_import

import logging
import warnings
import sys
import codecs
import six

from .exceptions import StoreDeprecationWarning


class InLevel(object):
    def __init__(self, level_list):
        self._level_list = level_list

    def filter(self, record):
        return record.levelno in self._level_list


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stdout = codecs.getwriter('utf-8')(sys.stdout)
    stderr = codecs.getwriter('utf-8')(sys.stderr)

    if not logging.root.handlers:
        stdout_handler = logging.StreamHandler(stream=stdout)
        stdout_handler.addFilter(InLevel([logging.INFO]))
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(logging.Formatter("%(message)s"))

        stderr_handler = logging.StreamHandler(stream=stderr)
        stderr_handler.addFilter(InLevel([logging.ERROR]))
        stderr_handler.setFormatter(logging.Formatter("%(message)s"))

        logger.addHandler(stdout_handler)
        logger.addHandler(stderr_handler)

    return logger


class LogMixin(object):
    logger = create_logger()

    def log(self, message):
        warnings.warn("The Store.log method has been replaced. Use Store.logger instead.", StoreDeprecationWarning)
        if not (message and isinstance(message, six.string_types)):
            return

        self.logger.info(message)
