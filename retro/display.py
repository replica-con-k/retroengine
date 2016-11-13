#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import retro.backend

_DEFAULT_SIZE_ = (1024, 768)
_DEFAULT_FPS_ = 60


class Display(object):
    def __init__(self, resolution=_DEFAULT_SIZE_, fps=_DEFAULT_FPS_):
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
            

def new(resolution=_DEFAULT_SIZE_, fps=_DEFAULT_FPS_):
    return Display(resolution, fps)
