import sys
import uuid
import logging
import warnings

import six

from .exceptions import StoreDeprecationWarning

class BaseStore(object):
    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.logger = logging.getLogger(__package__)
        self.initialize(stdout, stderr)

    def initialize(self, stdout, stderr):
        self._instructions = []
        self.stdout = stdout
        self.stderr = stderr

    def _instruction(self, type_, data):
        self._instructions.append({
            'id': str(uuid.uuid4()),
            'type': type_,
            'data': data,
        })


class Store(BaseStore):
    def log(self, message):
        warnings.warn("The Store.log method has been replaced. Use Store.logger instead.", StoreDeprecationWarning)
        if not (message and isinstance(message, six.string_types)):
            return

        self.logger.info(message)


class ActionStore(Store):
    def get(self, url, *args, **kwargs):
        return self._instruction('get', {
            'url': url,
            'args': args,
            'kwargs': kwargs
        })

    def redirect(self, url):
        return self._instruction('redirect', url)

    def to_dict(self):
        return {
            'instructions': self._instructions
        }
