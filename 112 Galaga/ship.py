# Creates ship class and gives it the appropiate methods

import pygame
from gameObject import GameObject

'''
Concept from GameObject.py and Ship.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids
'''

class Ship(GameObject):
    @staticmethod
    def init(screenWidth):
        Ship.size = int(screenWidth * 0.08) # 8% of the screen width
        Ship.shipImage = pygame.transform.scale(\
        pygame.image.load('images/ship.png').convert_alpha(), (Ship.size, Ship.size))

    def __init__(self, x, y, lives=2):
        super(Ship, self).__init__(x, y, Ship.shipImage, Ship.size)
        self.speed = 4
        self.lives = lives

    def getBucket(self, buckets, screenWidth):
        values = sorted(buckets.keys())
        cols = screenWidth // len(values)
        x = int(self.x // cols)
        key = values[x]
        return key

    def update(self, keysDown, screenWidth, buckets):
        bucket = self.getBucket(buckets, screenWidth)
        # move left or right but don't go off the screen
        if self.rect.left > 0:
            if keysDown(pygame.K_LEFT):
                self.x += self.speed * -1
                buckets[bucket].append(-1)
        else:
            if keysDown(pygame.K_RIGHT):
                self.x += self.speed
                buckets[bucket].append(1)

        if self.rect.right < screenWidth:
            if keysDown(pygame.K_RIGHT):
                self.x += self.speed
                buckets[bucket].append(1)
        else:
            if keysDown(pygame.K_LEFT):
                self.x += self.speed * -1
                buckets[bucket].append(-1)
        self.updateRect()

    def hurt(self, startX, startY):
        if self.lives > 0:
            return Ship(startX, startY, self.lives-1)
        else:
            return []
