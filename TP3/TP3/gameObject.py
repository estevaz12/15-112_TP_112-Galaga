# Basic class for all game objects

'''
From https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids
'''

import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        self.x, self.y, self.image, self.radius = x, y, image, int(radius * 0.45)
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
