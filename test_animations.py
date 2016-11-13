#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import retro
import retro.actors
import retro.assets
import retro.scenes
import retro.resources

class Movement1(retro.actors.Static):
    def update(self):
        self.position = (self.position[0] + 1,
                         self.position[1] + 1)
        return self.area

class Movement2(retro.actors.Static):
    def update(self):
        self.position = (self.position[0] - 1,
                         self.position[1] + 1)
        return self.area

def main():
    display = retro.new_display()
    
    background_image = retro.assets.load('background.jpg')
    scenario = retro.scenes.Static2DCollisions(background_image)
    scenario.destination = display
    
    actor_anim = retro.assets.load('pelusilla_*.png')
    actor_anim.fps = 10
    pelusa1 = Movement1(actor_anim.loop())
    pelusa2 = Movement2(actor_anim.pingpong().loop())
    scenario.spawn_actor(pelusa1, (-200, -200))
    scenario.spawn_actor(pelusa2, (800, -200))
        
    for frameno in range(1000):
        display.update(scenario.update())
        
if __name__ == '__main__':
    main()
