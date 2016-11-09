#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import backend

class Image(object):
    def __init__(self, layer):
        self.layer = layer

    @property
    def size(self):
        return self.layer.get_size()

    @property
    def bounding_box(self):
        return self.layer.get_bounding_rect()
    
def black_image(size, transparent=True):
    layer = backend.new_layer(self.__size)
    layer.fill((0, 0, 0, 0 if transparent else 255))
    return Image(layer)
