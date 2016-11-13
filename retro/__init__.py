#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import backend
backend.init_backend()

import display

def new_display(*args, **kwargs):
    return display.new(*args, **kwargs)
