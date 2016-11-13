#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import retro.backend


DEFAULT_RESOLUTION = (1024, 768)
DEFAULT_FPS = 60
CURRENT_FPS = DEFAULT_FPS

class Display(object):
    def __init__(self, resolution=DEFAULT_RESOLUTION, fps=DEFAULT_FPS):
        self.__scr = retro.backend.set_mode(resolution)
        self.__clock = retro.backend.new_clock()
        self.__fps = fps
        self.__size = self.__scr.get_size()

    @property
    def display(self):
        return self.__scr

    @property
    def size(self):
        return self.__size

    @property
    def fps(self):
        return self.__fps

    def blit(self, surface, position):
        self.__scr.blit(surface, position)

    def update(self, dirty_areas=None):
        self.__clock.tick(self.__fps)
        if dirty_areas is None:
            retro.backend.update_display()
        else:
            for area in dirty_areas:
                retro.backend.update_display(area)
            

def new(resolution=DEFAULT_RESOLUTION, fps=DEFAULT_FPS):
    global __CURRENT_FPS__
    __CURRENT_FPS__ = fps
    return Display(resolution, fps)

def get_game_fps():
    return __CURRENT_FPS__
