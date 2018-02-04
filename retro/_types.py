#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import uuid

from _const import WAITING_START, STARTED, KILLED


class GameObject(object):
    '''Every object in a game'''
    def __init__(self, **kwargs):
        self._id = str(uuid.uuid4())
        self._state = WAITING_START
        self._tags = set()
        self._scene = None
        if 'tags' in kwargs.keys():
            assert isinstance(kwargs['tags'], list)
            for tag in kwargs['tags']:
                self.add_tag(tag)
            kwargs.pop('tags')

    @property
    def id(self):
        return self._id

    @property
    def tags(self):
        return self._tags

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, new_scene):
        assert isinstance(new_scene, Scene) or (new_scene is None)
        self._scene = new_scene

    def add_tag(self, tag):
        assert(isinstance(tag, basestring))
        self._tags.add(tag)

    def remove_tag(self, tag):
        assert(isinstance(tag, basestring))
        self._tags.remove(tag)
        
    def is_tagged_as(self, tag):
        assert(isinstance(tag, basestring))
        return tag in self._tags
    
    def start(self):
        self.on_start()
        self._state = STARTED
        
    def kill(self):
        self.on_kill()
        self._state = KILLED

    @property
    def is_alive(self):
        return self._state in [WAITING_START, STARTED]

    @property
    def is_running(self):
        return self._state == STARTED

    @property
    def is_ready_to_start(self):
        return self._state == WAITING_START

    def on_start(self):
        '''Called before GameObject() start running'''
        pass

    def on_kill(self):
        '''Called before GameObject() is killed'''
        pass

    def update(self):
        '''Called every frame'''
        pass


class Scene(object):
    '''Every game part'''
    def __init__(self):
        self._game_object_ = {}

    @property
    def game_objects(self):
        return self._game_object_.values()

    def game_object(self, game_object_id):
        assert isinstance(game_object_id, basestring)
        return self._game_object_[game_object_id]

    def _cast_game_object_(self, game_object):
        if isinstance(game_object, basestring):
            return self.game_object(game_object)
        elif isinstance(game_object, GameObject):
            return game_object
        raise ValueError('Cannot cast object of type: %s' % type(game_object))

    def add_game_object(self, game_object, auto_start=True):
        assert isinstance(game_object, GameObject)
        self._game_object_[game_object.id] = game_object
        game_object.scene = self
        if auto_start and game_object.is_ready_to_start:
            game_object.start()
        return game_object.id

    def remove_game_object(self, game_object):
        game_object = self._cast_game_object_(game_object)
        game_object.scene = None
        del(self._game_object_[game_object.id])

    def game_objects_tagged_as(self, tag):
        return set(filter(lambda game_object: game_object.is_tagged_as(tag),
                          self._game_object_.values()))

    def update(self):
        '''Every frame update all game objects'''
        for game_object in self.game_objects:
            if not game_object.is_alive:
                self.remove_game_object(game_object)
                continue
            game_object.update()
