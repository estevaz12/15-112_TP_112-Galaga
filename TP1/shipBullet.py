import pygame
import math
from bullet import Bullet

'''
Concept from Bullet.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids
'''

class sBullet(Bullet):
    speed = 10

    @staticmethod
    def init():
        i = pygame.image.load('images/ship-bullet.png').convert_alpha()
        sBullet.image = pygame.transform.scale(i, (6, 16))
        sBullet.width, sBullet.height = sBullet.image.get_size()

    def __init__(self, x, y):
        super(sBullet, self).__init__(x, y, sBullet.image, sBullet.height)

    def update(self):
        self.y -= sBullet.speed
        self.updateRect()
        super(sBullet, self).update()
