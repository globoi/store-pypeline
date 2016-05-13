import json


class BaseStore(object):
    def __init__(self, redis=None, channel=None, log_method=None):
        self.initialize(redis, channel, log_method)

    def initialize(self, redis, channel, log_method):
        self.redis = redis
        self.channel = channel
        self.log_method = log_method

    def _action(self, type_, data):
        self.redis.publish(
            self.channel,
            json.dumps({
                'type': type_,
                'data': data,
            })
        )


class Store(BaseStore):
    def log(self, *args, **kwargs):
        self.log_method(*args, **kwargs)

    def get(self, url, *args, **kwargs):
        '''Method to request a url via browser'''
        return self._action('request', {
            'url': url,
            'args': args,
            'kwargs': kwargs
        })

    def redirect(self, url):
        return self._action('redirect', url)
