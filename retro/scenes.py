#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import backend
import resources

class Scenario(object):
    def __init__(self):
        self.actors = []
        self.destination = None

    def spawn_actor(self, actor, position=None):
        if position is not None:
            actor.position = position
        actor.scenario = self
        self.actors.append(actor)

    def update(self):
        raise NotImplementedError()
    

class Static2D(Scenario):
    def __init__(self, image_or_size):
        super(Static2D, self).__init__()
        self.offset = (0, 0)
        self.__gnd_portions = []       
        self.__dirty = []
        if isinstance(image_or_size, resources.Image):
            # 'image_or_size' is Image
            self.set_background(image_or_size)
        else:
            # 'image_or_size' is size (2-tuple)
            self.set_background(resources.black_image(image_or_size))

    def spawn_actor(self, actor, position=None):
        super(Static2D, self).spawn_actor(actor, position)
        self.__dirty.append(self._draw_actor_(actor))

    def set_background(self, image):
        '''Set background  and size of the scenario'''
        self.__size = image.size
        self.__gnd = image.layer
        self.__area = image.bounding_box
        self.__dirty = [self.__area]

    def _draw_actor_(self, actor):
        if not self.__area.colliderect(actor.area):
            return
        draw_area = self.__area.clip(actor.area)
        self.__gnd_portions.append(
            (self.__gnd.subsurface(draw_area).copy(), draw_area.topleft))
        return self.__gnd.blit(actor.layer, actor.position)

    def update(self):
        # Dirty areas for this frame
        dirty = self.__dirty

        # Restore previous background
        self.__gnd_portions.reverse()
        for portion, position in self.__gnd_portions:
            dirty.append(self.__gnd.blit(portion, position))
        self.__gnd_portions = []

        # Draw new frame
        live_actors = []
        for actor in self.actors:
            if actor.is_dead:
                continue
            live_actors.append(actor)
            actor.update()
            dirty_area = self._draw_actor_(actor)
            if dirty_area is None:
                continue
            dirty.append(dirty_area)

        # Draw dirty areas only
        self.__dirty = []
        if self.destination is None:
            return dirty
        self.destination.blit(self.__gnd, self.offset)
        return dirty


class Static2DCollisions(Static2D):
    def update(self):
        dirty = super(Static2DCollisions, self).update()
        for actor in self.actors:
            if actor.ethereal:
                continue
            target_actors = filter(lambda x: x is not actor,
                                   self.actors)
            collisions = actor.area.collidelistall(
                [target.area for target in target_actors])
            # Notify
            for collision in collisions:
                target = target_actors[collision]
                if not target.ethereal:
                    target.hit_by(actor)
        return dirty


