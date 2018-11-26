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

    def __init__(self, shipX, shipY, enemy):
        super(eBullet, self).__init__(enemy.x, enemy.y, eBullet.image, eBullet.height)
        o = shipX - enemy.x # opposite
        a = shipY - enemy.y # adjacent
        self.angle = math.atan(o/a)

    def update(self):
        self.x += eBullet.speed * self.angle
        self.y += eBullet.speed
        self.updateRect()
        super(eBullet, self).update()
