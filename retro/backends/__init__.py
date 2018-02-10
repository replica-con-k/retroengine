#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-


def new_virtual_console():
    '''VirtualConsole Factory'''
    # INFO: At the beggining only pygame backend is going to be implemented
    #       but more backends are planned.
    import pygame_backend
    return pygame_backend.VirtualConsole()
