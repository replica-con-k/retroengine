#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

class Actor(object):
    def __init__(self):
        self.scenario = None
        self.tags = []
        self.body = None

    @property
    def is_dead(self):
        return False

    def update(self):
        pass

    def hit_by(self, who):
        pass


class Drawable(Actor):
    def __init__(self, skin):
        super(Drawable, self).__init__()
        self.__position = (0, 0)
        self.skin = skin
        self.area = skin.bounding_box
        self.area.topleft = self.__position
        # By default
        self.body = self.area

    @property
    def layer(self):
        return self.skin.layer
    
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        self.__position = new_position
        self.area.topleft = new_position
        
    def update(self):
        return self.area


class Movable(Drawable):
    def __init__(self, skin):
        super(Movable, self).__init__(skin)
        self.__position = (0, 0)
        self.__moving_area = None

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        if self.__moving_area is not None:
            current_position = self.area.topleft
            self.area.topleft = new_position
            if not self.__moving_area.contains(self.area):
                # Cancel movement!
                self.area.topleft = current_position
                return
        else:
            self.area.topleft = new_position
        self.__position = new_position
            
    @property
    def moving_area(self):
        return self.__moving_area
        
    @moving_area.setter
    def moving_area(self, area):
        if not area.contains(self.area):
            # Object outside of new moving area!
            return
        self.__moving_area = area

    def move(self, offset_x=0, offset_y=0):
        self.position = (self.position[0] + offset_x,
                         self.position[1] + offset_y)
        
