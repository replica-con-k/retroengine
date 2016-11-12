#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import backend
import resources

class Scenario(object):
    def __init__(self):
        self.actors = []
        self.destination = None
        self.__top_scenario = None

    def show_on(self, destination):
        self.destination = destination

    def stack(self, scenario):
        self.__top_scenario = scenario
        # Move actors to the upper scenario
        self.__top_scenario.actors += self.actors
        self.__top_scenario.show_on(self.destination)

    @property
    def is_stacked(self):
        return self.__top_scenario is not None

    def spawn_actor(self, actor, position=None):
        if position is not None:
            actor.position = position
        actor.scenario = self
        self.actors.append(actor)
        if self.__top_scenario is not None:
            self.__top_scenario.actors.append(actor)

    def update(self):
        if self.__top_scenario is not None:
            return self.__top_scenario.update()
        return []


class Static2D(Scenario):
    def __init__(self, image_or_size):
        super(Static2D, self).__init__()
        self.offset = (0, 0)
        self.__gnd_portions = []       
        self.__dirty = []
        self.__fade_factor = None
        self.__fade_frame = None
        if isinstance(image_or_size, resources.Image):
            # 'image_or_size' is Image
            self.set_background(image_or_size)
        else:
            # 'image_or_size' is size (2-tuple)
            self.set_background(resources.black_image(image_or_size))

    def stack(self, scenario, fade_in=None):
        super(Static2D, self).stack(scenario)
        if fade_in is not None:
            scenario.set_fade_in(fade_in)

    def set_fade_in(self, fade_in):
        self.alpha = 255 if fade_in is None else 0
        if isinstance(fade_in, int):
            self.__fade_factor = 255.0 / float(fade_in)
            self.__fade_frame = 0
        self.__dirty += [self.__area]
        
    def show_on(self, destination, fade_in=None):
        super(Static2D, self).show_on(destination)
        if fade_in is not None:
            self.set_fade_in(fade_in)

    @property
    def is_on_fade(self):
        return self.alpha < 255

    @property
    def alpha(self):
        return self.__gnd.get_alpha()

    @alpha.setter
    def alpha(self, new_alpha):
        self.__gnd.set_alpha(new_alpha)
        self.__dirty.append(self.__area)

    def spawn_actor(self, actor, position=None):
        super(Static2D, self).spawn_actor(actor, position)
        self.__dirty.append(self.__gnd.blit(self.__gnd, (0, 0)))

    def set_background(self, image):
        '''Set background  and size of the scenario'''
        self.__size = image.size
        self.__gnd = image.layer#.copy().convert_alpha()
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
        dirty = super(Static2D, self).update()
        if self.is_stacked:
            return dirty
        
        # Dirty areas for this frame
        dirty += self.__dirty

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

        # Compute alpha
        if self.__fade_factor is not None:
            new_alpha = int(self.__fade_factor * self.__fade_frame)
            self.__fade_frame += 1
            if new_alpha >= 255:
                self.__fade_factor = None
                self.__fade_frame = None
            self.alpha = new_alpha

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


