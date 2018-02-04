#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import pytest

import retro

TAG1 = 'tag1'
TAG2 = 'tag2'


class TestGameObject:
    
    def test_creation(self):
        '''Create new GameObject() and check its initial state'''
        go = retro.GameObject()
        assert isinstance(go, retro.GameObject)
        assert go.scene is None
        assert not go.is_running
        assert go.is_alive
        assert len(go.tags) == 0

    def test_creation_with_tags(self):
        '''Create new GameObject() with initial tags'''
        go = retro.GameObject(tags=[TAG1])
        assert isinstance(go, retro.GameObject)
        assert go.scene is None
        assert not go.is_running
        assert go.is_alive
        assert TAG1 in go.tags
        assert go.is_tagged_as(TAG1)

    def test_starting(self):
        '''Start a GameObject() and check its state'''
        go = retro.GameObject()
        go.start()
        assert go.is_running
        assert go.is_alive
        
    def test_killing(self):
        '''Kill a GameObject() and check its state'''
        go = retro.GameObject()
        go.kill()
        assert not go.is_alive
        assert not go.is_running

    def test_tagging1(self):
        '''Add tag in a GameObject()'''
        go = retro.GameObject()
        go.add_tag(TAG1)
        assert TAG1 in go.tags
        assert go.is_tagged_as(TAG1)

    def test_tagging2(self):
        '''Add and remove several tags in a GameObject()'''
        go = retro.GameObject()
        go.add_tag(TAG1)
        go.add_tag(TAG2)
        assert go.is_tagged_as(TAG1) and go.is_tagged_as(TAG2)
        go.remove_tag(TAG1)
        assert not go.is_tagged_as(TAG1)
        assert go.is_tagged_as(TAG2)

    def test_tagging3(self):
        '''Remove unknown tags in a GameObject()'''
        go = retro.GameObject()
        assert not go.is_tagged_as(TAG1)
        with pytest.raises(KeyError):
            go.remove_tag(TAG1)
            
    def test_on_start(self):
        '''Check if on_start() is executed'''
        class MyGameObject(retro.GameObject):
            '''This class demonstrate de use of on_start()'''
            def __init__(self):
                super(MyGameObject, self).__init__()
                self.on_start_called = False

            def on_start(self):
                self.on_start_called = True

        go = MyGameObject()
        assert isinstance(go, retro.GameObject)
        go.start()
        assert go.is_running
        assert go.on_start_called

    def test_on_kill(self):
        '''Check if on_kill() is executed'''
        class MyGameObject(retro.GameObject):
            '''This class demonstrate de use of on_kill()'''
            def __init__(self):
                super(MyGameObject, self).__init__()
                self.on_kill_called = False

            def on_kill(self):
                self.on_kill_called = True

        go = MyGameObject()
        assert isinstance(go, retro.GameObject)
        go.kill()
        assert not go.is_alive
        assert go.on_kill_called
