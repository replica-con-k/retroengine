#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import uuid
import threading

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
    def __init__(self, name):
        self._name_ = name
        self._game_object_ = {}
        self._game_ = None

    @property
    def name(self):
        return self._name_

    @property
    def game(self):
        return self._game_

    @game.setter
    def game(self, new_game):
        assert isinstance(new_game, Game)
        self._game_ = new_game
        
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

    def add_game_object(self, game_object, auto_start=False):
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

    def start(self):
        self.on_start()
        for game_object in self.game_objects:
            if game_object.is_ready_to_start:
                game_object.start()

    def update(self):
        '''Every frame update all game objects'''
        for game_object in self.game_objects:
            if not game_object.is_alive:
                self.remove_game_object(game_object)
                continue
            game_object.update()

    def on_start(self):
        '''Called before Scene() start running'''
        pass
    

class Game(threading.Thread):
    '''The game itself'''
    def __init__(self, initial_scene):
        super(Game, self).__init__()
        assert isinstance(initial_scene, Scene)
        initial_scene.game = self
        self.__scenes__ = {
            initial_scene.name: initial_scene
        }
        self.__current_scene__ = initial_scene.name
        self._running_ = False
        self._tick_ = 0

    @property
    def current_scene(self):
        return self.__scenes__[self.__current_scene__]

    @property
    def scenes(self):
        return self.__scenes__.keys()

    @property
    def running(self):
        return self._running_

    @property
    def ticks(self):
        return self._tick_
    
    def add_scene(self, scene):
        assert isinstance(scene, Scene)
        scene.game = self
        self.__scenes__[scene.name] = scene
        
    def switch_scene(self, scene_name):
        if scene_name not in self.__scenes__.keys():
            raise KeyError(scene_name)
        self.__current_scene__ = scene_name

    def start(self):
        self._running_ = True
        super(Game, self).start()
        
    def run(self):
        while self._running_:
            self.current_scene.update()
            self._tick_ += 1

    def quit(self):
        self._running_ = False
