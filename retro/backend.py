#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import pygame
import resources

EVENT_QUIT = pygame.QUIT
EVENT_KEY_PRESS = pygame.KEYDOWN
EVENT_KEY_RELEASE = pygame.KEYUP
EVENT_MOUSE_PRESS = pygame.MOUSEBUTTONDOWN
EVENT_MOUSE_RELEASE = pygame.MOUSEBUTTONUP
EVENT_MOUSE_MOVE = pygame.MOUSEMOTION

def init_backend():
    pygame.init()

def end_backend():
    pygame.quit()

def set_mode(size):
    return pygame.display.set_mode(size,
                                   pygame.HWSURFACE)

def new_layer(size):
    return pygame.Surface(size, pygame.HWSURFACE|pygame.SRCALPHA)

def load_image(image_name):
    srf = resources.Image(pygame.image.load(image_name).convert())
    return srf

def load_sound(sound_name):
    return pygame.mixer.Sound(sound_name)

def load_animation(image_list, fps=1):
    # Animation is converted to alpha (so set_alpha() will not work)
    layers = [pygame.image.load(image).convert_alpha() for image in image_list]
    return resources.Animation(layers, fps)

def update_display(area=None):
    if not area:
        pygame.display.flip()
    else:
        pygame.display.update(area)

def new_clock():
    return pygame.time.Clock()

class Event(object):
    def __init__(self, ev_type, data, as_str='unknown'):
        self.type = ev_type
        self.as_dict = data
        # Only for debug purposes
        self.as_str = as_str
    # Only for debug purposes
    def __str__(self):
        return self.as_str

def wait_event():
    event = pygame.event.wait()
    return Event(event.type, event.dict, str(event))

def clear_controller_events():
    return pygame.event.clear()
