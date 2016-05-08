#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of store_pypeline.
# https://github.com/rfloriano/store-pypeline

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Rafael Floriano da Silva rflorianobr@gmail.com

import json
import os
import re
import exec_pypeline
from redis.sentinel import Sentinel


class Pipeline(exec_pypeline.Pipeline):

    def __init__(self, action_list):
        super(Pipeline, self).__init__(action_list, before_action=self.before_action, after_action=self.after_action)
        sentinel_hosts = re.findall('((?:\d{1,3}\.?){4})', os.environ['SENTINEL_HOSTS'])
        sentinel_hosts = zip(sentinel_hosts[0::2], sentinel_hosts[1::2])
        self.redis = Sentinel(sentinel_hosts).master_for(os.environ['REDIS_MASTER'])
        self.actions_channel = os.environ['ACTIONS']
        self.stdout_channel = os.environ['STDOUT']
        self.stderr_channel = os.environ['STDERR']
        self.notify_actions()
        self._failed_action = None
        self._failed_err = None

    def before_action(self, act, ctx, failed):
        self.notify_actions()

    def after_action(self, act, ctx, failed):
        self.notify_actions()

    def notify_actions(self):
        data = {'actions': []}
        for i, action in enumerate(self.action_list):
            d = action.to_dict()
            d.update({'index': i})
            data['actions'].append(d)
        self.redis.publish(self.actions_channel, json.dumps(data))
