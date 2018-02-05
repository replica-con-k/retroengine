#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import pytest

import retro

TAG1 = 'tag1'
TAG2 = 'tag2'

class TestScene:

    def test_creation(self):
        '''Create new Scene() and check its initial state'''
        scene = retro.Scene('test_scene')
        assert isinstance(scene, retro.Scene)
        assert scene.game is None
        assert len(scene.game_objects) == 0

    def test_add_game_object(self):
        '''Add GameObject() to a scene'''
        scene = retro.Scene('test_scene')
        game_object = retro.GameObject()
        scene.add_game_object(game_object)
        assert len(scene.game_objects) == 1
        assert game_object is scene.game_object(game_object.id)
        assert game_object.scene is scene

    def test_remove_game_object(self):
        '''Test remove GameObject() from a scene'''
        scene = retro.Scene('test_scene')
        game_object = retro.GameObject()
        scene.add_game_object(game_object)
        scene.remove_game_object(game_object)
        assert len(scene.game_objects) == 0

    def test_remove_unknown_game_object(self):
        '''Remove GameObject() not added to a scene'''
        scene = retro.Scene('test_scene')
        game_object = retro.GameObject()
        with pytest.raises(KeyError):
            scene.remove_game_object(game_object)

    def test_search_game_object_by_tags(self):
        '''Search game objects by tags'''
        scene = retro.Scene('test_scene')
        game_object1 = retro.GameObject()
        game_object2 = retro.GameObject(tags=[TAG1])
        game_object3 = retro.GameObject(tags=[TAG1, TAG2])
        scene.add_game_object(game_object1)
        scene.add_game_object(game_object2)
        scene.add_game_object(game_object3)
        assert game_object1 not in scene.game_objects_tagged_as(TAG1)
        assert game_object1 not in scene.game_objects_tagged_as(TAG2)        
        assert game_object2 in scene.game_objects_tagged_as(TAG1)
        assert game_object2 not in scene.game_objects_tagged_as(TAG2)
        assert game_object3 in scene.game_objects_tagged_as(TAG1)
        assert game_object3 in scene.game_objects_tagged_as(TAG2)
        
    def test_update_function(self):
        '''Test if update() is called on every GameObject() objects'''
        class MyGameObject(retro.GameObject):
            def __init__(self):
                super(MyGameObject, self).__init__()
                self.update_called = False

            def update(self):
                self.update_called = True

        scene = retro.Scene('test_scene')
        game_object1 = MyGameObject()
        game_object2 = MyGameObject()
        scene.add_game_object(game_object1)
        assert not game_object1.update_called
        assert not game_object2.update_called        
        scene.update()
        assert game_object1.update_called
        assert not game_object2.update_called        

    def test_garbage_collector(self):
        '''Test if Scene() removes dead GameObject() objects'''
        scene = retro.Scene('test_scene')
        game_object = retro.GameObject()
        scene.add_game_object(game_object)
        assert game_object in scene.game_objects
        game_object.kill()
        scene.update()
        assert game_object not in scene.game_objects
