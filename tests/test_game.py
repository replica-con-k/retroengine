#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import time
import pytest

import retro

INITIAL_SCENE = 'test_scene'
OTHER_SCENE = 'other_scene'

class TestGame:

    def test_creation(self):
        '''Create new Game() and check its initial state'''
        game = retro.Game(retro.Scene(INITIAL_SCENE))
        assert isinstance(game, retro.Game)
        assert not game.running
        assert game.current_scene.name == INITIAL_SCENE
        assert game.current_scene.game is game

    def test_running(self):
        '''Create new Game() and start it'''
        game = retro.Game(retro.Scene(INITIAL_SCENE))
        game.start()
        assert game.running
        tick1 = game.ticks
        time.sleep(1.0)
        tick2 = game.ticks
        game.quit()
        assert not game.running
        assert tick2 > tick1

    def test_add_scene(self):
        '''Create Game() and add several Scene() objects'''
        game = retro.Game(retro.Scene(INITIAL_SCENE))
        game.add_scene(retro.Scene(OTHER_SCENE))
        assert set([INITIAL_SCENE, OTHER_SCENE]) == set(game.scenes)

    def test_switch_scene(self):
        '''Create Game() with several Scene() objects and switch them'''
        game = retro.Game(retro.Scene(INITIAL_SCENE))
        game.add_scene(retro.Scene(OTHER_SCENE))
        assert game.current_scene.name == INITIAL_SCENE
        game.switch_scene(OTHER_SCENE)
        assert game.current_scene.name == OTHER_SCENE

    def test_switch_unknown_scene(self):
        '''Create Game() and switch to a unknown scene'''
        game = retro.Game(retro.Scene(INITIAL_SCENE))
        with pytest.raises(KeyError):
            game.switch_scene(OTHER_SCENE)
                       
