#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

__VERSION__ = 0.1


import threading


class VirtualConsole(threading.Thread):
    '''
    Virtual retro gaming device
    '''
    def __init__(self):
        super(VirtualConsole, self).__init__()
        self.__state = State()
        self.__screen = None
        self.__powered = False

    @property
    def powered(self):
        return self.__powered
    
    @property
    def state(self):
        return self.__state

    @property
    def screen(self):
        return self.__screen

    def power_on(self):
        self.__powered = True
        self.start()

    def power_off(self):
        self.__state = None
        self.__screen = None
        self.__powered = False
        
    def run(self):
        self.power_off()


class State(dict):
    def __init__(self, *args, **kwargs):
        super(State, self).__init__(*args, **kwargs)
