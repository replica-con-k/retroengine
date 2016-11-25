#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import backend
import threading

_EVENT_HANDLER_ = None

def _no_op_():
    pass

_CALLBACKS_ = {
    'on_quit': _no_op_,
}

class ControllerHandler(threading.Thread):
    def __init__(self):
        super(ControllerHandler, self).__init__()
        self.running = True
        self.user_want_to_quit = False

        self.__pointer_position__ = (0, 0)

    @property
    def pointer_position(self):
        return self.__pointer_position__

    def stop(self):
        self.running = False
        backend.clear_controller_events()
        
    def run(self):
        while self.running:
            event = backend.wait_event()
            if event.type == backend.EVENT_QUIT:
                self.user_want_to_quit = True
                _CALLBACKS_['on_quit']()
                continue
            elif event.type == backend.EVENT_MOUSE_PRESS:
                self.__refresh_mouse_position__(event.as_dict)
                continue
            elif event.type == backend.EVENT_MOUSE_MOVE:
                self.__refresh_mouse_position__(event.as_dict)
                continue
            print event

    def __refresh_mouse_position__(self, event):
        self.__pointer_position__ = event['pos']


def init_controllers():
    global _EVENT_HANDLER_
    _EVENT_HANDLER_ = ControllerHandler()
    _EVENT_HANDLER_.start()

def close_controllers():
    global _EVENT_HANDLER_
    _EVENT_HANDLER_.stop()
    _EVENT_HANDLER_.join()
    _EVENT_HANDLER_ = None

def is_controller_ready():
    return _EVENT_HANDLER_ is not None

def user_want_to_quit():
    if is_controller_ready:
        return _EVENT_HANDLER_.user_want_to_quit

def set_callback(cb_id, callback):
    global _CALLBACKS_
    _CALLBACKS_[cb_id] = callback

def remove_callback(cb_id):
    _CALLBACKS_[cb_id] = _no_op_

def pointer():
    return _EVENT_HANDLER_.pointer_position
