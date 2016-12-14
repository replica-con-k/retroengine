#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

def _no_op_(who):
    pass

def action(action_implementation):
    '''Decorator to switch skin auto'''
    def wrapped(*args):
        args[0].skin.do(action_implementation.__name__)
        return action_implementation(*args)
    return wrapped
    
class Actor(object):
    def __init__(self, skin):
        self.skin = skin
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
        super(Drawable, self).__init__(skin)
        self.__position = (0, 0)
        self.area = self.skin.bounding_box
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
        self.on_cancel_movement = _no_op_

        self.speed_x = 0
        self.speed_y = 0

        self.__current_action__ = None
        self.current_action = self.default

    @property
    def current_action(self):
        return self.__current_action__

    @current_action.setter
    def current_action(self, new_action_cb):
        if new_action_cb != self.__current_action__:
            self.__current_action__ = new_action_cb

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
                self.on_cancel_movement(self)
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

    def _move_(self):
        self.position = (self.position[0] + self.speed_x,
                         self.position[1] + self.speed_y)

    @action
    def swap(self, offset_x=0, offset_y=0):
        self.position = (self.position[0] + offset_x,
                         self.position[1] + offset_y)

    @action    
    def up(self, new_speed=None):
        self.speed_y = -new_speed or self.speed_y
        self._move_()

    @action
    def down(self, new_speed=None):
        self.speed_y = new_speed or self.speed_y
        self._move_()

    @action
    def left(self, new_speed=None):
        self.speed_x = -new_speed or self.speed_x
        self._move_()

    @action
    def right(self, new_speed=None):
        self.speed_x = new_speed or self.speed_x
        self._move_()
        
    @action
    def stop(self, x_axis=True, y_axis=True):
        if x_axis:
            self.speed_x = 0
        if y_axis:
            self.speed_y = 0

    @action
    def default(self):
        self._move_()

    def update(self):
        self.current_action()
        return super(Movable, self).update()
