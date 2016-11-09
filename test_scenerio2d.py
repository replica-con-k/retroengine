#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

import pygame

import retro
import retro.actors
import retro.scenes
import retro.backend
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
    pygame.init()
    display = pygame.display.set_mode((1024, 768))
    
    background_image = retro.backend.load_image('assets/background.jpg')
    scenario = retro.scenes.Static2DCollisions(background_image)
    scenario.destination = display
    
    ball_image = retro.backend.load_image('assets/ball.png')
    ball1 = Movement1(ball_image)
    ball2 = Movement2(ball_image)
    scenario.spawn_actor(ball1, (-200, -200))
    scenario.spawn_actor(ball2, (800, -200))
        
    for frameno in range(1000):
        pygame.display.update(scenario.update())
        
if __name__ == '__main__':
    main()
    
