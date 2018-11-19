import pygame
from gameObject import GameObject

'''
Concept from Bullet.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids
'''

class Bullet(GameObject):
    speed = 10

    @staticmethod
    def init():
        i = pygame.image.load('images/ship-bullet.png').convert_alpha()
        Bullet.image = pygame.transform.scale(i, (6, 16))
        Bullet.width, Bullet.height = Bullet.image.get_size()

    def __init__(self, x, y):
        super(Bullet, self).__init__(x, y, Bullet.image, Bullet.height)

    def update(self, screenHeight):
        self.y -= Bullet.speed
        self.updateRect()
