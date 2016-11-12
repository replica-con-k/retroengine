#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import pygame
import resources

def new_layer(size):
    return pygame.Surface(size, pygame.HWSURFACE|pygame.SRCALPHA)

def load_image(image_name):
    srf = resources.Image(pygame.image.load(image_name).convert())#_alpha())
    return srf

