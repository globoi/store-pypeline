from __future__ import absolute_import

import sys
import uuid

import six

from .logging import LogMixin


class BaseStore(object):
    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
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


class Store(BaseStore, LogMixin):
    pass


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
