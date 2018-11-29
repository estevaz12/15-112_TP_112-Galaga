import pygame
import math
import random
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

    def __init__(self, x, y, enemy, difficulty):
        super(eBullet, self).__init__(enemy.x, enemy.y, eBullet.image, eBullet.height)
        self.xDest = x
        self.yDest = y
        self.enemyX = enemy.x
        self.enemyY = enemy.y
        o = self.xDest - self.enemyX # opposite
        a = self.yDest - self.enemyY # adjacent
        self.angle = math.atan(o/a)

        self.speed = random.randint(5, 10)
        if difficulty == "easy":
            self.speed = random.randint(5, 8)
        elif difficulty == "normal":
            self.speed = random.randint(6, 9)
        elif difficulty == "hard":
            self.speed = random.randint(7, 10)

    def update(self):
        self.x += self.speed * self.angle
        self.y += self.speed
        self.updateRect()
        super(eBullet, self).update()
