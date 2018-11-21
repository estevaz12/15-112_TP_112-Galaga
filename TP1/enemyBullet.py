import pygame
import math
from bullet import Bullet

'''
Concept from Bullet.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids
'''

class eBullet(Bullet):
    @staticmethod
    def init():
        i = pygame.image.load('images/enemy-bullet.png').convert_alpha()
        eBullet.image = pygame.transform.scale(i, (6, 16))
        eBullet.width, eBullet.height = eBullet.image.get_size()

    def __init__(self, ship, enemy):
        super(eBullet, self).__init__(enemy.x, enemy.y, eBullet.image, eBullet.height)
        o = ship.x - enemy.x # opposite
        a = ship.y - enemy.y # adjacent
        # if o < 0:
        #     self.xDir = -1
        # elif o > 0:
        #     self.xDir = 1
        self.angle = math.atan(o/a)

    def update(self):
        self.x += eBullet.speed * self.angle
        self.y += eBullet.speed
        self.updateRect()
        super(eBullet, self).update()
