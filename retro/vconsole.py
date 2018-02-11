#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import retro.backends
import retro.backends.interfaces


class NoConsole(retro.backends.interfaces.VirtualConsole):
    '''This is not a console'''
    @property
    def powered(self):
        return False

    @property
    def screen(self):
        return None

    @property
    def state(self):
        return None

    @property
    def sprite_manager(self):
        return None
    
_CONSOLE_ = NoConsole()
screen = _CONSOLE_.screen
state = _CONSOLE_.state


def power_on():
    '''Initialize backend and VirtualConsole fields'''
    global screen
    global state
    global _CONSOLE_

    if _CONSOLE_.powered:
        # Already powered on!
        return

    _CONSOLE_ = retro.backends.new_virtual_console()
    state = _CONSOLE_.state
    screen = _CONSOLE_.screen
    _CONSOLE_.power_on()


def power_off():
    '''Shutdown backend and destroy VirtualConsole fields'''
    global screen
    global state
    global _CONSOLE_

    if not _CONSOLE_.powered:
        # Already powered off!
        return

    _CONSOLE_.power_off()


def is_powered():
    '''Return if VirtualConsole is active or not'''
    return _CONSOLE_.powered
