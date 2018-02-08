#!/usr/bin/env python
#

_POWERED_ = False

screen = None
state = None


def power_on():
    '''Initialize backend and VirtualConsole fields'''
    global screen
    global state
    global _POWERED_

    if _POWERED_:
        # Already powered on!
        return
    _POWERED_ = True
    state = {}


def power_off():
    '''Shutdown backend and destroy VirtualConsole fields'''
    global screen
    global state
    global _POWERED_

    if not _POWERED_:
        # Already powered off!
        return

    _POWERED_ = False
    state = None


def is_powered():
    '''Return if VirtualConsole is active or not'''
    return _POWERED_
