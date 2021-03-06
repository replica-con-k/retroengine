#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import retro
import retro.actors
import retro.assets
import retro.scenes
import retro.resources
import retro.controller
import retro.puppeteers

class Player(retro.actors.Movable):
    def update(self):
        self.position = retro.controller.pointer()
        return self.area

def main():
    display = retro.new_display()
    retro.controller.init()
    player = retro.puppeteers.Player()

    background_image = retro.assets.load('background.jpg')
    scenario = retro.scenes.Static2DCollisions(background_image)
    scenario.destination = display
    
    actor_anim = retro.assets.load('pelusilla_*.png')
    actor_anim.fps = 10
    actor_skin = retro.resources.Skin(
        animations={
            'default': actor_anim.loop()
            })
    pelusa = retro.actors.Movable(actor_skin)
    player.add_actor(pelusa)
    scenario.spawn_actor(pelusa, (200, 200))

    frameno = 0
    while not retro.controller.user_want_to_quit():
        display.update(scenario.update())
        frameno += 1
        if frameno > 8000:
            break
    retro.controller.stop()
        
if __name__ == '__main__':
    main()
