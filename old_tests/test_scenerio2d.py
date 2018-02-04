#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import retro
import retro.actors
import retro.assets
import retro.scenes
import retro.resources

class Movement1(retro.actors.Drawable):
    def update(self):
        self.position = (self.position[0] + 1,
                         self.position[1] + 1)
        return self.area

class Movement2(retro.actors.Drawable):
    def update(self):
        self.position = (self.position[0] - 1,
                         self.position[1] + 1)
        return self.area

def main():
    display = retro.new_display()
    
    background_image = retro.assets.load('background.jpg')
    scenario = retro.scenes.Static2DCollisions(background_image)
    scenario.destination = display
    
    ball_image = retro.assets.load('ball.png')
    ball1 = Movement1(ball_image)
    ball2 = Movement2(ball_image)
    scenario.spawn_actor(ball1, (-200, -200))
    scenario.spawn_actor(ball2, (800, -200))
        
    for frameno in range(1000):
        display.update(scenario.update())
        
if __name__ == '__main__':
    main()
