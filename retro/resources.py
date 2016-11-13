#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import backend
import display

class Image(object):
    def __init__(self, layer):
        self.layer = layer
        self.layer.set_alpha(255)

    @property
    def size(self):
        return self.layer.get_size()

    @property
    def bounding_box(self):
        return self.layer.get_bounding_rect()


class Animation(Image):
    def __init__(self, layers=[], fps=1):
        self.layers = layers
        self.__size = self._compute_size_()
        self.__rect = self._compute_rect_()
        self.__current_frame = 0
        self.__top_frame = len(self.layers) - 1
        self.__ended = False
        self.__fps = None
        self.__current_tick = 0
        self.fps = fps

    def _compute_size_(self):
        h_res = [layer.get_size()[0] for layer in self.layers]
        v_res = [layer.get_size()[1] for layer in self.layers]
        return (max(h_res), max(v_res))

    def _compute_rect_(self):
        if len(self.layers) == 0:
            return None
        bounding_box = self.layers[0].get_bounding_rect()
        for layer in self.layers[1:]:
            bounding_box.union_ip(layer.get_rect())
        return bounding_box
        
    @property
    def size(self):
        return self.__size

    @property
    def bounding_box(self):
        return self.__rect
    
    @property
    def ended(self):
        return self.__ended
    
    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, fps):
        self.__fps = fps
        self.__ticks_per_frm = round(
            float(display.CURRENT_FPS)/float(fps))

    def copy(self):
        return self.sequence()

    def reverse(self):
        layers = []
        for layer in self.layers:
            layers.append(layer.copy())
        layers.reverse()
        return Animation(layers, self.fps)

    def pingpong(self):
        return self.copy() + self.reverse()

    def sequence(self):
        layers = []
        for layer in self.layers:
            layers.append(layer.copy())
        return Animation(layers, self.fps)
        
    def loop(self):
        layers = []
        for layer in self.layers:
            layers.append(layer.copy())
        return Loop(layers, self.fps)
    
    def reset(self):
        self.__current_frame = 0
        self.__ended = False

    @property
    def layer(self):
        self.__current_tick += 1
        if self.__current_tick >= self.__ticks_per_frm:
            self.__current_tick = 0
            return self.next_layer
        return self.layers[self.__current_frame]

    @property
    def next_layer(self):
        if self.__current_frame == self.__top_frame:
            self.__ended = True
        frame = self.layers[self.__current_frame]
        if self.__current_frame < self.__top_frame:
            self.__current_frame += 1
        return frame

    def __add__(self, animation):
        if type(animation) != type(self):
            raise ValueError()
        layers = []
        for layer in self.layers + animation.layers:
            layers.append(layer.copy())
        return Animation(layers, self.fps)

    def __iadd__(self, animation):
        return self.__add__(animation)


class Loop(Animation):
    def copy(self):
        layers = []
        for layer in self.layers:
            layers.append(layer.copy())
        return Loop(layers, self.fps)

    def reverse(self):
        layers = []
        for layer in self.layers:
            layers.append(layer.copy())
        layers.reverse()
        return Loop(layers, self.fps)

    def pingpong(self):
        return self.copy() + self.reverse()

    def __add__(self, animation):
        if type(animation) != type(self):
            raise ValueError()
        layers = []
        for layer in self.layers + animation.layers:
            layers.append(layer.copy())
        return Loop(layers, self.fps)

    def __iadd__(self, animation):
        return self.__add__(animation)

    @property
    def layer(self):
        frame = super(Loop, self).layer
        if self.ended:
            self.reset()
        return frame


def black_image(size, transparent=True):
    layer = backend.new_layer(self.__size)
    layer.fill((0, 0, 0, 0 if transparent else 255))
    return Image(layer)
