#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import actors
import controller

class Puppeteer(object):
    def __init__(self):
        self.actors = []
        self.__n_actors = 0

    def add_actor(self, actor):
        if actor in self.actors:
            return
        self.actors.append(actor)
        self.__n_actors += 1

    @property
    def count(self):
        return self.__n_actors
        
    def update(self):
        # Remove dead actors
        live_actors = []
        for actor in filter(lambda a: not a.is_dead, self.actors):
            actor.update()
            if actor.is_dead:
                continue
            live_actors.append(actor)
        self.actors = live_actors


class UniformMove(Puppeteer):
    def __init__(self):
        super(UniformMove, self).__init__()
        self.__area = None

    def add_actor(self, actor):
        if not isinstance(actor, actors.Movable):
            # Cannot add non-movable actors
            # LOG THIS
            return
        super(UniformMove, self).add_actor(actor)

    @property
    def moving_area(self):
        return self.__area

    @moving_area.setter
    def moving_area(self, area):
        self.__area = area
        for actor in self.actors:
            actor.moving_area = self.__area

    def move(self, offset_x=0, offset_y=0):
        for actor in self.actors:
            actor.move(offset_x, offset_y)

    @property
    def speed_x(self):
        if self.count == 0:
            return 0
        return sum([a.speed_x for a in self.actors]) / self.count

    @property
    def speed_y(self):
        if self.count == 0:
            return 0
        return sum([a.speed_y for a in self.actors]) / self.count

    @speed_x.setter
    def speed_x(self, new_speed_x):
        for actor in self.actors:
            actor.speed_x = new_speed_x

    @speed_x.setter
    def speed_y(self, new_speed_y):
        for actor in self.actors:
            actor.speed_y = new_speed_y


P1_KEYS={
    'up': 111,
    'down': 116,
    'left': 113,
    'right': 114
    }


class Player(UniformMove):
    def __init__(self, scancodes=P1_KEYS):
        super(Player, self).__init__()
        self.__scancodes = scancodes
        self.__controller_id = controller.register_player(self)

    def __del__(self):
        # Player collected by gbc
        controller.unregister_player(self.__controller_id)
    
    def controller_handler(self, event):
        if event.type == controller.START:
            scancode = event.as_dict['scancode']
            if scancode == self.__scancodes.get('up', None):
                self.__all_start_up()
            elif scancode == self.__scancodes.get('down', None):
                self.__all_start_down()
            elif scancode == self.__scancodes.get('left', None):
                self.__all_start_left()
            elif scancode == self.__scancodes.get('right', None):
                self.__all_start_right()
        elif event.type == controller.STOP:
            scancode = event.as_dict['scancode']
            if scancode == self.__scancodes.get('up', None):
                self.__all_stop_up()
            elif scancode == self.__scancodes.get('down', None):
                self.__all_stop_down()
            elif scancode == self.__scancodes.get('left', None):
                self.__all_stop_left()
            elif scancode == self.__scancodes.get('right', None):
                self.__all_stop_right()

    def __all_start_up(self):
        self.speed_y = -1
    
    def __all_start_down(self):
        self.speed_y = 1
    
    def __all_start_left(self):
        self.speed_x = -1
    
    def __all_start_right(self):
        self.speed_x = 1
    
    def __all_stop_up(self):
        self.speed_y = 0
    
    def __all_stop_down(self):
        self.speed_y = 0
    
    def __all_stop_left(self):
        self.speed_x = 0
        
    def __all_stop_right(self):
        self.speed_x = 0
