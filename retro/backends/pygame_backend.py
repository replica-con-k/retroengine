#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

try:
    import pygame
except ImportError:
    raise ImportError('''
For now this is the only implemeneted backend so it's required for the
Retroengine. If more backends could be available this exception should
be catched to continue loading''')


import retro.backends.interfaces


__VERSION__ = 0.1


class VirtualConsole(retro.backends.interfaces.VirtualConsole):
    '''
    Implementation written in pygame
    '''
    def __init__(self):
        super(VirtualConsole, self).__init__()

    def run(self):
        while self.powered:
            pass
        
