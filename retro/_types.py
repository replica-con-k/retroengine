#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import uuid

from _const import WAITING_START, STARTED, KILLED


class GameObject(object):
    def __init__(self):
        self._id = str(uuid.uuid4())
        self._state = WAITING_START
        self._tags = set()

    @property
    def id(self):
        return self._id

    @property
    def tags(self):
        return self._tags

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

    def on_start(self):
        '''Called before GameObject() start running'''
        pass

    def on_kill(self):
        '''Called before GameObject() is killed'''
        pass

    def update(self):
        '''Called every frame'''
        pass
