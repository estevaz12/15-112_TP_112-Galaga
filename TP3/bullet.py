import pygame
import math
import random
from gameObject import GameObject

class Bullet(GameObject):
    speed = 5
    time = 50 * 2 # 4 seconds

    def __init__(self, x, y, image, size):
        super(Bullet, self).__init__(x, y, image, size)
        self.timeOnScreen = 0

    def update(self):
        self.timeOnScreen += 1
        if self.timeOnScreen > Bullet.time:
            self.kill()

'''
Concept from Bullet.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids
'''
class sBullet(Bullet):
    speed = 8

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
