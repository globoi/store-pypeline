import json


class BaseStore(object):
    def __init__(self, redis=None, channel=None, stderr=None):
        self.initialize(redis, channel, stderr)

    def initialize(self, redis, channel, stderr):
        self.redis = redis
        self.channel = channel
        self.stderr = stderr

    def _action(self, type_, data):
        self.redis.publish(
            self.channel,
            json.dumps({
                'type': type_,
                'data': data,
            })
        )


class Store(BaseStore):
    def log(self, message):
        self.stderr.write(message + '\n')
        self.stderr.flush()

    def get(self, url, *args, **kwargs):
        '''Method to request a url via browser'''
        return self._action('request', {
            'url': url,
            'args': args,
            'kwargs': kwargs
        })

    def redirect(self, url):
        return self._action('redirect', url)
