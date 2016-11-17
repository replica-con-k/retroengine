#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import backend
import display

class Sound(object):
    def __init__(self, sound):
        self.snd = sound
        
class Image(object):
    def __init__(self, layer):
        self.layer = layer
        self.__bounding_box = layer.get_bounding_rect()
        self.layer.set_alpha(255)

    @property
    def size(self):
        return self.bounding_box.size

    @property
    def bounding_box(self):
        return self.__bounding_box


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


class Skin(object):
    def __init__(self, animations={}, default='default', sounds={}):
        assert(default in animations.keys())
        self.__anims = animations
        self.__sounds = sounds
        self.__default_action = default
        self.__current = None
        self.do(default)

    @property
    def layer(self):
        return self.__anims[self.__current].layer

    @property
    def bounding_box(self):
        return self.__anims[self.__current].bounding_box

    @property
    def size(self):
        return self.__anims[self.__current].size

    def clone(self):
        anims = {}
        sounds = {}
        for action in self.actions:
            anims[action] = self[action].copy()
            if action in self.__sounds.keys():
                sounds[action] = self.__sounds[action]
        return Skin(anims, self.default_action, sounds)

    @property
    def default_action(self):
        return self.__default_action

    @default_action.setter
    def default_action(self, new_action):
        assert(new_action in self.actions)
        self.__default_action = new_action
        
    @property
    def action(self):
        return self.__current

    @property
    def actions(self):
        return self.__anims.keys()

    @property
    def ended(self):
        return self.__anims[self.__current].ended

    def reset(self, animation=None):
        animation = animation or self.__default
        self.do(animation)

    def do(self, animation):
        if animation == self.__current:
            return
        assert(animation in self.actions)
        self.__current = animation
        self.__anims[self.__current].reset()
        snd = self.__sounds.get(self.__current, no_sound())
        snd.play()

    def add_action(self, action, animation, sound=None):
        self.__anims[action] = animation
        if sound is not None:
            self.__sounds[action] = sound
            
    def __getitem__(self, key):
        return self.__anims[key]

    def __setitem__(self, key, value):
        self.add_action(key, value)


def black_image(size, transparent=True):
    layer = backend.new_layer(self.__size)
    layer.fill((0, 0, 0, 0 if transparent else 255))
    return Image(layer)


def no_sound():
    class DummySound(object):
        def play(self):
            pass
    return DummySound()
