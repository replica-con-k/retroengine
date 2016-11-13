#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import pygame
import resources

def init_backend():
    pygame.init()

def end_backend():
    pygame.quit()

def set_mode(size):
    return pygame.display.set_mode(size,
                                   pygame.FULLSCREEN|pygame.HWSURFACE)

def new_layer(size):
    return pygame.Surface(size, pygame.HWSURFACE|pygame.SRCALPHA)

def load_image(image_name):
    srf = resources.Image(pygame.image.load(image_name).convert())
    return srf

def load_animation(image_list, fps=1):
    layers = [pygame.image.load(image).convert_alpha() for image in image_list]
    return resources.Animation(layers, fps)

def update_display(area=None):
    if not area:
        pygame.display.flip()
    else:
        pygame.display.update(area)

def new_clock():
    return pygame.time.Clock()
