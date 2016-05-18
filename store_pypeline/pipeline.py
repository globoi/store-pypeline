#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of store_pypeline.
# https://github.com/rfloriano/store-pypeline

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Rafael Floriano da Silva rflorianobr@gmail.com

import json
import os
import sys
import re

import exec_pypeline
from store_pypeline import store
from redis.sentinel import Sentinel


class Pipeline(exec_pypeline.Pipeline, store.Store):
    action_list = None

    def __init__(self, action_list=None, sentinel_hosts=None, redis_master=None,
                 stdout=sys.stdout, redis_session=None, pipeline=None,
                 stderr=sys.stderr):

        self.pipeline = pipeline
        if pipeline is None:
            self.pipeline = json.loads(os.environ.get('PIPELINE', 'null'))
            if self.pipeline is None:
                self.pipeline = []

        if redis_session is None:
            if sentinel_hosts is None:
                sentinel_hosts = os.environ['SENTINEL_HOSTS']

            if redis_master is None:
                redis_master = os.environ['REDIS_MASTER']

            sentinel_hosts = re.findall('((?:\d{1,3}\.?){4})', sentinel_hosts)
            sentinel_hosts = zip(sentinel_hosts[0::2], sentinel_hosts[1::2])
            self.redis = Sentinel(sentinel_hosts).master_for(redis_master)
        else:
            self.redis = redis_session

        self.stdout = stdout
        self.stderr = stderr
        exec_pypeline.Pipeline.__init__(self, action_list, before_action=self.before_action, after_action=self.after_action)
        store.Store.__init__(self, self.redis, stdout, self.stderr)
        self._set_redis_for_actions()
        self.notify_actions()
        self._failed_action = None
        self._failed_err = None

    def _set_redis_for_actions(self):
        for action in self.action_list:
            action.initialize(self.redis, self.channel, self.stderr)

    def before_forward(self, act, ctx, exception):
        self.log(act.name)

    def before_backward(self, act, ctx, exception):
        if exception:
            self.log(act.to_dict().get('error', {}).get('traceback'))

    def actions_to_dict(self, *args, **kwargs):
        actions = super(Pipeline, self).actions_to_dict(*args, **kwargs)
        return self.pipeline + actions

    def before_action(self, act, ctx, exception):
        self.notify_actions()

    def after_action(self, act, ctx, exception):
        self.notify_actions()

    def notify_actions(self):
        self.stdout.write(json.dumps(self.actions_to_dict()))
        self.stdout.flush()
