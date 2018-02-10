#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import time
import pytest

import retro.vconsole
from retro.backends.interfaces import State

INITIAL_SCENE = 'test_scene'
OTHER_SCENE = 'other_scene'

class TestVConsole:

    def test_initial_state(self):
        '''Check if VConsole is disabled initially'''
        assert not retro.vconsole.is_powered()
        assert retro.vconsole.state is None
        assert retro.vconsole.screen is None                

    def test_power_on(self):
        '''Check if VConsole can be powered on'''
        retro.vconsole.power_on()
        assert retro.vconsole.is_powered()
        assert isinstance(retro.vconsole.state, State)

    def test_double_power_on(self):
        '''Check if VConsole can be already powered on'''
        assert retro.vconsole.is_powered()
        retro.vconsole.power_on()
        assert retro.vconsole.is_powered()

    def test_power_off(self):
        '''Check if VConsole can be powered off'''
        assert retro.vconsole.is_powered()
        retro.vconsole.power_off()
        assert not retro.vconsole.is_powered()
        assert retro.vconsole.screen is None
        
    def test_double_power_off(self):
        '''Check if VConsole can be already powered off'''
        assert not retro.vconsole.is_powered()
        retro.vconsole.power_off()
        assert not retro.vconsole.is_powered()
        assert retro.vconsole.screen is None
        
