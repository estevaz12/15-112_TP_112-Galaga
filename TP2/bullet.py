import pygame
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
