#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import retro
from retro import controller

class DummyPlayer(object):
    def controller_handler(self, event):
        print 'Type: %s Data: %s' % (event.type, event.as_dict)

def main():
    display = retro.new_display()
    controller.init()
    controller.register_player(DummyPlayer())
    
    while not controller.user_want_to_quit():
        pass
    controller.stop()

if __name__ == '__main__':
    main()
