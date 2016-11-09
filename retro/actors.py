#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

class Actor(object):
    def __init__(self):
        self.scenario = None
        self.tags = []
        self.ethereal = False

    @property
    def is_dead(self):
        return False

    def update(self):
        pass

    def hit_by(self, who):
        pass


class Static(Actor):
    def __init__(self, skin):
        super(Static, self).__init__()
        self.__position = (0, 0)
        self.layer = skin.layer
        self.area = self.layer.get_rect()
        self.area.topleft = self.__position

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        self.__position = new_position
        self.area.topleft = new_position
        
    def update(self):
        return self.area


