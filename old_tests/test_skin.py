#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import retro
import retro.actors
from retro.actors import action
import retro.assets
import retro.scenes
import retro.resources


class Movement1(retro.actors.Drawable):
    def update(self):
        self.position = (self.position[0] + 1,
                         self.position[1] + 1)
        return self.area

    def hit_by(self, who):
        self.smashed()

    @action
    def smashed(self):
        pass

    
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
    
    normal_anim = retro.assets.load('pelusilla_*.png').loop()
    smashed_anim = normal_anim.pingpong()
    normal_anim.fps = smashed_anim.fps = 10
    pelusa_skin = retro.resources.Skin(
        animations={
            'default': normal_anim,
            'smashed': smashed_anim
        }, sounds={
            'smashed': retro.assets.load('punch.ogg')
        })
    
    pelusa1 = Movement1(pelusa_skin.clone())
    pelusa2 = Movement2(pelusa_skin.clone())
    scenario.spawn_actor(pelusa1, (-10, -10))
    scenario.spawn_actor(pelusa2, (800, -10))
        
    for frameno in range(500):
        display.update(scenario.update())
        
if __name__ == '__main__':
    main()
