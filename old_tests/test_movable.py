#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import pygame

import retro
import retro.actors
import retro.assets
import retro.scenes
import retro.resources

class Pelusa(retro.actors.Movable):
    def hit_by(self, who):
        self.skin.do('smashed')

def main():
    display = retro.new_display()
    
    background_image = retro.assets.load('background.jpg')
    scenario = retro.scenes.Static2DCollisions(background_image)
    scenario.destination = display
    
    normal_anim = retro.assets.load('pelusilla_*.png').loop()
    smashed_anim = normal_anim.pingpong()
    normal_anim.fps = smashed_anim.fps = 10
    punch = retro.assets.load('punch.ogg')
    pelusa_skin = retro.resources.Skin(
        animations={
            'default': normal_anim,
            'down': normal_anim,
            'left': normal_anim,
            'right': normal_anim,
            'smashed': smashed_anim
        }, sounds={
            'smashed': punch
        })
    
    pelusa1 = Pelusa(pelusa_skin.clone())
    pelusa1.moving_area = display.area
    pelusa1.down(1)
    pelusa1.right(2)
    pelusa2 = Pelusa(pelusa_skin.clone())
    pelusa2.moving_area = display.area
    pelusa2.left(1)
    pelusa2.down(2)
    scenario.spawn_actor(pelusa1, (0, 0))
    scenario.spawn_actor(pelusa2, (800, 0))
        
    for frameno in range(500):
        display.update(scenario.update())
        
if __name__ == '__main__':
    main()
