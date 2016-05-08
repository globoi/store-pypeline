#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of store_pypeline.
# https://github.com/rfloriano/store-pypeline

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Rafael Floriano da Silva rflorianobr@gmail.com

import sys
import json
import os
import re
import pypeline
import traceback
from redis.sentinel import Sentinel


class Pipeline(pypeline.Pipeline):

    def __init__(self, action_list):
        super(Pipeline, self).__init__(action_list, before_action=self.before_action, after_action=self.after_action,
                                       on_failed=self.on_failed)
        sentinel_hosts = re.findall('((?:\d{1,3}\.?){4})', os.environ['SENTINEL_HOSTS'])
        sentinel_hosts = zip(sentinel_hosts[0::2], sentinel_hosts[1::2])
        self.redis = Sentinel(sentinel_hosts).master_for(os.environ['REDIS_MASTER'])
        self.actions_channel = os.environ['ACTIONS']
        self.stdout_channel = os.environ['STDOUT']
        self.stderr_channel = os.environ['STDERR']
        self.notify_actions()
        self._failed_action = None
        self._failed_err = None

    def publish_action(self, act):
        self.redis.publish(self.actions_channel, act.to_dict())

    def before_action(self, act, ctx, failed):
        self.notify_actions()

    def after_action(self, act, ctx, failed):
        self.notify_actions()

    # def after_action(self, act, ctx, failed):
    #     self.publish_action(act)
    #     last_action = self.action_list[0] if failed else self.action_list[-1]
    #     if act == last_action:
    #         self.redis.publish(self.actions_channel, "JOB-FINISHED")
    #         if failed:
    #             msg = 'Failed when execute {0} forward'.format(self._failed_action.__class__.__name__)
    #             self.redis.publish(self.stderr_channel, traceback.format_exc(self._failed_err))
    #             self.redis.publish(self.stderr_channel, msg)
    #             sys.exit(1)

    def on_failed(self, act, ctx, e):
        self.publish_action(act)
        self._failed_action = act
        self._failed_err = e

    def notify_actions(self):
        data = {'actions': []}
        for i, action in enumerate(self.action_list):
            d = action.to_dict()
            d.update({'index': i})
            data['actions'].append(d)
        self.redis.publish(self.actions_channel, json.dumps(data))


class Action(pypeline.Action):
    pass
