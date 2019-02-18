# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals
from os import environ
from mock import MagicMock, patch
from store_pypeline import Action, Pipeline

from .base import TestCase


class PipelineTestCase(TestCase):
    
    def test_before_forward_should_write_unicode_caracer(self):
        """
        This problem occurs when PYTHONIOENCODING is not utf-8
        """
        # arrange
        action = Action(name='🙄')
        action.forward = MagicMock()
        action.backward = MagicMock()
        action_list = [action]
        context = {}
        # act and assert
        pipeline = Pipeline(action_list)
        try:
            pipeline.before_forward(action, context)
        except UnicodeEncodeError:
            self.fail("before_forward() raised UnicodeEncodeError unexpectedly!")

    def test_before_backward_should_write_unicode_caracer(self):
        """
        This problem occurs when PYTHONIOENCODING is not utf-8
        """
        # arrange
        action = Action(name='🙄')
        action.forward = MagicMock()
        action.backward = MagicMock()
        action_list = [action]
        context = {}
        # act and assert
        pipeline = Pipeline(action_list)
        try:
            pipeline.before_backward(action, context)
        except UnicodeEncodeError:
            self.fail("before_backward() raised UnicodeEncodeError unexpectedly!")
