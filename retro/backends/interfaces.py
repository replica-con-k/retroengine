#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

__VERSION__ = 0.1


import copy
import threading
import collections


class VirtualConsole(threading.Thread):
    '''
    Virtual retro gaming device
    '''
    def __init__(self):
        super(VirtualConsole, self).__init__()
        self.__state = State()
        self.__sprite_manager = SpriteManager()
        self.__screen = None
        self.__powered = False

    @property
    def state(self):
        return self.__state

    @property
    def sprite_manager(self):
        return self.__sprite_manager

    @property
    def screen(self):
        return self.__screen

    @property
    def powered(self):
        return self.__powered
    
    def power_on(self):
        self.__powered = True
        self.start()

    def power_off(self):
        self.__state = None
        self.__screen = None
        self.__powered = False
        
    def run(self):
        self.power_off()


class State(object):
    '''
    Contains all data used in the game
    '''
    def __init__(self):
        self.__state__ = {}
        self.__save_state__ = {}

    def save(self, name):
        self.__save_state__[name] = copy.copy(self.__state__)

    def load(self, name):
        if name not in self.__save_state__.keys():
            raise ValueError('State not found: %s' % name)
        self.__state__ = copy.copy(self.__save_state__[name])

    @property
    def saves(self):
        return self.__save_state__.keys()

    def clear(self):
        self.__state__ = {}

    def keys(self):
        return self.__state__.keys()

    def values(self):
        return self.__state__.values()

    def __contains__(self, key):
        return key in self.keys()
    
    def __getitem__(self, key):
        return self.__state__[key]

    def __setitem__(self, key, value):
        self.__state__[key] = value

    def __delitem__(self, key):
        del(self.__state__[key])

    def get(self, key, default_value):
        return self.__state__.get(key, default_value)

    def update(self, other):
        self.__state__.update(other)


class SpriteManager(object):
    '''
    Handling 2D sprites
    '''
    def __init__(self):
        self.__textures__ = collections.OrderedDict()
        
        self.__frame_stack__ = collections.OrderedDict()

    def add(self, name, texture):
        self.__texture__[name] = texture

    @property
    def sprites(self):
        return self.__textures__.keys()

    def draw(self, name, position):
        if name not in self.sprites:
            raise ValueError('Texture not found')
        self.__frame_stack__.append(name, position)

    def render(self, canvas):
        for sprite_name, position in self.__frame_stack__:
            canvas.put(self.__textures__[sprite_name], position)
        # This "clear" the canvas for the next frame,
        # maybe should be called in other method
        self.__frame_stack__ = collections.OrderedDict()


class Display(object):
    '''
    Show game content
    '''
    def __init__(self):
        pass

    @property
    def width(self):
        return None

    @property
    def height(self):
        return None

    @property
    def top(self):
        return None

    @property
    def bottom(self):
        return None

    @property
    def left(self):
        return None

    @property
    def right(self):
        return None
    
    def update(self):
        pass
    
