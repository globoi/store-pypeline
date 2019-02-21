#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of store_pypeline.
# https://github.com/rfloriano/store-pypeline

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Rafael Floriano da Silva rflorianobr@gmail.com
from __future__ import absolute_import

import warnings

from .pipeline import Pipeline
from .action import Action
from .exceptions import StoreDeprecationWarning


warnings.simplefilter("default", StoreDeprecationWarning)
