#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

import uuid
import backend
import threading

START = backend.EVENT_KEY_PRESS
STOP = backend.EVENT_KEY_RELEASE

_EVENT_HANDLER_ = None

def _no_op_():
    pass

# Callbacks
#
_CALLBACKS_ = {
    'on_quit': _no_op_,
    'on_click': _no_op_
}

class ControllerHandler(threading.Thread):
    def __init__(self):
        super(ControllerHandler, self).__init__()
        self.__pointer_position__ = (0, 0)
        self.__listeners = {}

        self.running = True
        self.user_want_to_quit = False
        self.subscribe(self.__handle_engine_events__)

    def subscribe(self, callback):
        cb_id = str(uuid.uuid4())
        self.__listeners[cb_id] = callback
        return cb_id

    def unsubscribe(self, callback_id):
        if callback_id in self.__listeners.keys():
            del(self.__listeners[callback_id])

    def _broadcast_(self, event):
        for callback in self.__listeners.values():
            callback(event)

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
                _CALLBACKS_.get('on_quit', _no_op_)()
                continue
            # Unknown event
            self._broadcast_(event)            

    def __handle_engine_events__(self, event):
        if event.type in [backend.EVENT_MOUSE_PRESS, backend.EVENT_MOUSE_MOVE]:
            self.__refresh_mouse_position__(event.as_dict)
        
    def __refresh_mouse_position__(self, event):
        self.__pointer_position__ = event['pos']


def init():
    global _EVENT_HANDLER_
    _EVENT_HANDLER_ = ControllerHandler()
    _EVENT_HANDLER_.start()

def stop():
    global _EVENT_HANDLER_
    _EVENT_HANDLER_.stop()
    _EVENT_HANDLER_.join()
    _EVENT_HANDLER_ = None

def is_ready():
    return _EVENT_HANDLER_ is not None

def user_want_to_quit():
    if is_ready():
        return _EVENT_HANDLER_.user_want_to_quit

def set_callback(cb_id, callback):
    global _CALLBACKS_
    _CALLBACKS_[cb_id] = callback

def remove_callback(cb_id):
    _CALLBACKS_[cb_id] = _no_op_

def pointer():
    return _EVENT_HANDLER_.pointer_position

def register_player(player):
    if not is_ready():
        return
    return _EVENT_HANDLER_.subscribe(player.controller_handler)
    
def unregister_player(controller_id):
    if not is_ready():
        return
    _EVENT_HANDLER_.unsubscribe(controller_id)
