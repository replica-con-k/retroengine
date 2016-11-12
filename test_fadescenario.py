#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import time
import pygame

import retro
import retro.assets
import retro.scenes
import retro.backend
import retro.resources

def main():
    pygame.init()
    display = pygame.display.set_mode((1024, 768))#, pygame.HWSURFACE)
    
    background1 = retro.assets.load('fade_layer_background1.png')
    background2 = retro.assets.load('fade_layer_background2.png')

    scenario = retro.scenes.Static2DCollisions(background1)
    scenario.show_on(display)
    pygame.display.update(scenario.update())
    print 'Wait 2s'
    time.sleep(2.0)

    print 'Fading...'
    FADE_LENGHT=1000 # Float=time, Int=number_of_frames
        
    lighted_scenario = retro.scenes.Static2DCollisions(background2)
    scenario.stack(lighted_scenario, fade_in=FADE_LENGHT)

    while lighted_scenario.is_on_fade:
        pygame.display.update(scenario.update())

    pygame.display.update(scenario.update())
    print 'Wait 2s'
    time.sleep(2.0)
    pygame.quit()
        
if __name__ == '__main__':
    main()
    
